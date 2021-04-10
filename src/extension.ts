import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
	const defaultTriggerChars = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

	let functions = require('../resources/functions.json');
	functions.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Function);

	let defines = require('../resources/defines.json');
	defines.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Constant);

	let typedefs = require('../resources/typedefs.json');
	typedefs.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Interface);

	let enumerations = require('../resources/enumerations.json');
	enumerations.forEach((element: vscode.CompletionItem) => element.kind = vscode.CompletionItemKind.Enum);

	let enumMembers = require('../resources/enum_members.json');
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

	context.subscriptions.push(vscode.languages.registerSignatureHelpProvider('cuda', {
		provideSignatureHelp(document, position, token, context) {
			const triggerText = document.getText(new vscode.Range(document.positionAt(0), position));
			let offset = document.offsetAt(position);
			let paramsCount = 0;
			let parenCount = 0;
			for (let index = offset - 1; index > 0; index--) {
				switch (triggerText[index]) {
					case ",":
						if (parenCount === 0) {
							paramsCount++;
						}
						break;
					case ")":
						parenCount++;
						break;
					case "(":
						if (parenCount > 0) {
							parenCount--;
						}
						else {
							// provide signature help
							const range = document.getWordRangeAtPosition(document.positionAt(index - 1));
							const functionName = document.getText(range);
							const functionIndex = functions.map((e: { label: any; }) => e.label).indexOf(functionName);
							if (functionIndex !== -1) {
								return {
									signatures: [
										{
											label: functions[functionIndex].detail,
											parameters: functions[functionIndex].parameters
										}
									],
									activeSignature: 0,
									activeParameter: paramsCount
								};
							}
						}
						break;
					default:
						break;
				}
			}

			return undefined;
		}
	}, '(', ','));
}

export function deactivate() { }
