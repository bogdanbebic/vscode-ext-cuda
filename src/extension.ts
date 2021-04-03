import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
	const defaultTriggerChars = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

	let functions = require('../spider_output/functions.json');
	functions.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Function);

	let defines = require('../spider_output/defines.json');
	defines.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Constant);

	let typedefs = require('../spider_output/typedefs.json');
	typedefs.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Interface);

	let enumerations = require('../spider_output/enumerations.json');
	enumerations.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Enum);

	let enumMembers = require('../spider_output/enum_members.json');
	enumMembers.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.EnumMember);

	let allItems = functions.concat(defines, typedefs, enumerations, enumMembers);

	context.subscriptions.push(vscode.languages.registerCompletionItemProvider('cuda', {
		provideCompletionItems(document, position, token, context) {
			return new vscode.CompletionList(allItems);
		}
	}, defaultTriggerChars));

	context.subscriptions.push(vscode.languages.registerHoverProvider('cuda', {
		provideHover(document, position, token) {
			const range = document.getWordRangeAtPosition(position);
			const word = document.getText(range);
			let index = allItems.map((e: { label: any; }) => e.label).indexOf(word);
			if (index !== -1) {
				return new vscode.Hover(
					`\`${allItems[index].detail}\`\n\n${allItems[index].documentation}`,
					range
				);
			}

			return undefined;
		}
	}));
}

export function deactivate() { }
