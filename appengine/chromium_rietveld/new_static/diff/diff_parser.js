// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

"use strict";

function DiffParser(text)
{
    this.lines = text.split("\n");
    this.currentLine = 0;
    Object.preventExtensions(this);
}

DiffParser.HEADER_BEGIN = "Index: ";
DiffParser.TEXT_HEADER_END = "+++ ";
DiffParser.BINARY_HEADER_END = "Binary files ";
DiffParser.COPY_FROM_PREFIX = "copy from ";
DiffParser.COPY_TO_PREFIX = "copy to ";
DiffParser.RENAME_FROM_PREFIX = "rename from ";
DiffParser.RENAME_TO_PREFIX = "rename to ";
DiffParser.HEADER_PATTERN = /^@@ \-(\d+),[^+]+\+(\d+)(,\d+)? @@ ?(.*)/;
DiffParser.IMAGE_EXTENSIONS = {
    "png": true,
    "jpeg": true,
    "jpg": true,
    "webp": true,
    "bmp": true,
    "gif": true,
};

DiffParser.isImageFile = function(name)
{
    var index = name.lastIndexOf(".");
    // Dot files are not images.
    if (index <= 0)
        return false;
    var extension = name.from(index + 1);
    return DiffParser.IMAGE_EXTENSIONS[extension] || false;
};

DiffParser.prototype.peekLine = function()
{
    return this.lines[this.currentLine];
};

DiffParser.prototype.takeLine = function(type)
{
    var line = this.lines[this.currentLine++];
    if (!type)
        return line;
    if (type == "add" || type == "remove" || type == "both")
        return line.slice(1);
    return line;
};

DiffParser.prototype.haveLines = function()
{
    return this.currentLine != this.lines.length;
};

DiffParser.prototype.nextLineType = function()
{
    var line = this.peekLine();
    if (!line.length)
        return "empty";
    var c = line[0];
    if (c == "@")
        return "header";
    if (c == "+")
        return "add";
    if (c == "-")
        return "remove";
    if (c == "I")
        return "index";
    if (c == " ")
        return "both";
    if (c == "\\")
        return "skip";
    throw new Error("Parse error: Unable to classify line: '{1}'".assign(line));
};

DiffParser.prototype.parseFile = function()
{
    var groups = [];
    var currentGroup = null;
    var currentBeforeLineNumber = 0;
    var currentAfterLineNumber = 0;
    var deltaOffset = 0;
    var removeCount = 0;
    while (this.haveLines()) {
        var type = this.nextLineType();
        if (type == "index" || type == "empty")
            break; // We're done with this file.

        if (type == "skip") {
            this.currentLine++
            continue;
        }

        var groupType = type;
        var line = new DiffLine(type);

        if (groupType == "header") {
            var matchedHeader = this.takeLine().match(DiffParser.HEADER_PATTERN);
            var beforeLineNumber = parseInt(matchedHeader[1], 10);
            var afterLineNumber = parseInt(matchedHeader[2], 10);
            line.contextLinesStart = currentBeforeLineNumber + deltaOffset;
            line.contextLinesEnd = beforeLineNumber - 1 + deltaOffset;
            line.context = line.contextLinesEnd > 0;
            line.text = matchedHeader[4];
            currentBeforeLineNumber = beforeLineNumber;
            currentAfterLineNumber = afterLineNumber;
            if (!beforeLineNumber)
                continue;
        } else {
            line.beforeNumber = currentBeforeLineNumber;
            line.afterNumber = currentAfterLineNumber;
            line.text = this.takeLine(type);

            if (groupType == "remove" || groupType == "both")
                currentBeforeLineNumber++;
            if (groupType == "add" || groupType == "both")
                currentAfterLineNumber++;
        }

        if (groupType == "remove")
            removeCount++;
        else if (groupType == "add" && removeCount)
            removeCount--;
        else if (groupType == "add")
            deltaOffset++;
        else
            removeCount = 0;

        if (groupType == "add" || groupType == "remove")
            groupType = "delta";
        if (!currentGroup || groupType != currentGroup.type) {
            if (currentGroup)
                groups.push(currentGroup);
            currentGroup = new DiffGroup(groupType);
        }
        currentGroup.addLine(line);
    }
    if (currentGroup)
        groups.push(currentGroup);

    // Always have a header at the end of the file to allow an "Expand context"
    // link to show the rest of the file after the last group.
    var endLine = new DiffLine("header");
    endLine.contextLinesStart = currentBeforeLineNumber + deltaOffset;
    endLine.contextLinesEnd = Number.MAX_SAFE_INTEGER;
    endLine.context = true;
    groups.push(new DiffGroup("header", [endLine]));

    return groups;
};

DiffParser.prototype.parseHeader = function()
{
    var header = {
        isBinary: false,
        from: "",
        to: "",
    };
    while (this.haveLines()) {
        var line = this.takeLine();
        if (line.startsWith(DiffParser.TEXT_HEADER_END)) {
            header.isBinary = false;
            break;
        } else if (line.startsWith(DiffParser.BINARY_HEADER_END)) {
            header.isBinary = true;
            break;
        } else if (line.startsWith(DiffParser.COPY_FROM_PREFIX)
            || line.startsWith(DiffParser.RENAME_FROM_PREFIX)) {
            header.from = line;
        } else if (line.startsWith(DiffParser.COPY_TO_PREFIX)
            || line.startsWith(DiffParser.RENAME_TO_PREFIX)) {
            header.to = line;
        }
    }
    return header;
};

DiffParser.prototype.parse = function()
{
    var result = [];
    while (this.haveLines()) {
        var line = this.takeLine();
        if (!line.startsWith(DiffParser.HEADER_BEGIN))
            continue;
        var name = line.slice(DiffParser.HEADER_BEGIN.length);
        var header = this.parseHeader();
        var groups = this.parseFile();
        result.push({
            name: name,
            isImage: DiffParser.isImageFile(name),
            from: header.from,
            to: header.to,
            external: header.from && groups.length == 1,
            groups: groups,
        });
    }
    return result;
};
