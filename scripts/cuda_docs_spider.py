import scrapy
import re


class CudaDocsSpider(scrapy.Spider):
    name = "cuda_docs"

    custom_settings = {
        # "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 2,
    }

    start_urls = [
        "file:///C:/Users/Bogdan/Desktop/cuda-index.html",
    ]

    def parse(self, response):
        urls = response.xpath("//div[@class='body']//ul/li/a/@href").re(
            r".*group__CUDART.*"
        )
        self.logger.debug(f"docs urls found: {urls}")
        urls = [
            "file:///C:/Users/Bogdan/Desktop/cuda-page-1.html",
            "file:///C:/Users/Bogdan/Desktop/cuda-page-2.html",
        ]
        yield from response.follow_all(urls, callback=self.parse_docs)

    def parse_docs(self, response):
        groups = response.xpath("//div[@class='description']")
        headings = groups.xpath("h3//text()").getall()
        contents = groups.xpath("dl")
        for heading, content in zip(headings, contents):
            if heading == "Functions":
                parsed_contents = self._parse_content_functions(content)
            elif heading == "Defines":
                parsed_contents = self._parse_content_defines(content)
            elif heading == "Typedefs":
                parsed_contents = self._parse_content_typedefs(content)
            elif heading == "Enumerations":
                parsed_contents = self._parse_content_enumerations(content)
            else:
                self.logger.warning("Detected unknown heading:", heading)
            for parsed_entry in parsed_contents:
                yield parsed_entry

    def _parse_content_functions(self, selector):
        ret_lst = []
        function_selectors = selector.xpath("./dt")
        descr_selectors = selector.xpath("./dd")
        for func_selector, descr_selector in zip(function_selectors, descr_selectors):
            # Parse function signature
            template_signature = "".join(func_selector.xpath("./p//text()").getall())
            func_signature = "".join(func_selector.xpath("./span//text()").getall())
            func_signature = func_signature.replace("\u200b", "")
            # modifier, return_type, func_name, args_list
            signature_re = (
                r"(__host__|__device__|__host__\s+__device__)\s+(.+)\s+(\w+)\s+\((.*)\)"
            )
            m = re.match(signature_re, func_signature)
            modifier = " ".join(m[1].strip().split())
            return_type = m[2].strip()
            func_name = m[3].strip()
            args_list = " ".join(m[4].strip().split())
            name = func_name
            value = f"{modifier} {return_type} {func_name}({args_list})"
            if template_signature != "":
                value = f"{template_signature} {value}"
            # Parse description
            short_descr = "".join(
                descr_selector.xpath("./div")[0].xpath(".//text()").getall()
            )
            descr = short_descr
            # Not all functions have detailed documentation,
            # we add it if it exists
            if len(descr_selector.xpath("./div")) == 4:
                param_descr = "".join(
                    descr_selector.xpath("./div")[1].xpath(".//text()").getall()
                )
                returns_descr = "".join(
                    descr_selector.xpath("./div")[2].xpath(".//text()").getall()
                )
                descr += param_descr + returns_descr
            ret_lst.append(
                {
                    "kind": "function",
                    "name": name,
                    "value": value,
                    "descr": descr,
                }
            )
        return ret_lst

    def _parse_content_defines(self, selector):
        ret_lst = []
        define_selectors = selector.xpath("./dt/span")
        descr_selectors = selector.xpath("./dd/div/p")
        for define_selector, descr_selector in zip(define_selectors, descr_selectors):
            define_str = "".join(define_selector.xpath(".//text()").getall())
            define_list = define_str.split()
            name = define_list[1]
            value = define_list[2] if len(define_list) == 3 else ""
            descr = "".join(descr_selector.xpath(".//text()").getall())
            ret_lst.append(
                {
                    "kind": "define",
                    "name": name,
                    "value": value,
                    "descr": descr,
                }
            )
        return ret_lst

    def _parse_content_typedefs(self, selector):
        ret_lst = []
        typedef_selectors = selector.xpath("./dt/span")
        descr_selectors = selector.xpath("./dd/div/p")
        for typedef_selector, descr_selector in zip(typedef_selectors, descr_selectors):
            typedef_str = "".join(typedef_selector.xpath(".//text()").getall())
            typedef_list = typedef_str.split()
            if typedef_list[0] != "typedef":
                continue
            name = typedef_list[-1]
            value = " ".join(typedef_list[1:-1])
            descr = "".join(descr_selector.xpath(".//text()").getall())
            ret_lst.append(
                {
                    "kind": "typedef",
                    "name": name,
                    "value": value,
                    "descr": descr,
                }
            )
        return ret_lst

    def _parse_content_enumerations(self, selector):
        ret_lst = []
        enum_selectors = selector.xpath("./dt/span")
        descr_selectors = selector.xpath("./dd")
        for enum_selector, descr_selector in zip(enum_selectors, descr_selectors):
            enum_str = "".join(enum_selector.xpath(".//text()").getall())
            enum_list = enum_str.split()
            name = enum_list[1]
            descr = "".join(descr_selector.xpath("./div/p//text()").getall())
            ret_lst.append(
                {
                    "kind": "enum",
                    "name": name,
                    "descr": descr,
                }
            )
            members = self._parse_content_enum_members(descr_selector.xpath("./div/dl"))
            ret_lst += members
        return ret_lst

    def _parse_content_enum_members(self, selector):
        ret_lst = []
        member_selectors = selector.xpath("./dt/span")
        descr_selectors = selector.xpath("./dd")
        last_member_value = -1
        for member_selector, descr_selector in zip(member_selectors, descr_selectors):
            member_str = "".join(member_selector.xpath(".//text()").getall())
            member_list = member_str.split()
            name = member_list[0]
            if len(member_list) == 3:
                value = member_list[2]
            else:
                value = str(last_member_value + 1)
            last_member_value = int(value, 0)
            descr = "".join(descr_selector.xpath(".//text()").getall())
            ret_lst.append(
                {
                    "kind": "enum-member",
                    "name": name,
                    "value": value,
                    "descr": descr,
                }
            )
        return ret_lst
