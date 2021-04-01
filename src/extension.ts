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
}

export function deactivate() { }
