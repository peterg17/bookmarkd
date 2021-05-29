// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Traverse the bookmark tree, and print the folder and nodes.
function dumpBookmarks(arr) {
  var bookmarkTreeNodes = chrome.bookmarks.getTree(function (
    bookmarkTreeNodes
  ) {
    $("#bookmarks").append(dumpTreeNodes(bookmarkTreeNodes, arr));
    var firstTen = arr.slice(0, 10);
    console.log(`first 10 unsorted bookmarks are: ${JSON.stringify(firstTen)}`);
    arr.sort(function (a, b) {
      return a.id - b.id;
    });
    firstTen = arr.slice(0, 10);
    console.log(`first 10 sorted bookmarks are: ${JSON.stringify(firstTen)}`);
  });
}
function dumpTreeNodes(bookmarkNodes, arr) {
  var list = $("<ul>");
  var i;
  for (i = 0; i < bookmarkNodes.length; i++) {
    list.append(dumpNode(bookmarkNodes[i], arr));
  }
  return list;
}

/*
Step 1: Query backend on initialization for most recently received
bookmark id

Step 2: push all bookmarks into flat array, sort by id
find most recently received bookmark id or -1 (which means
none have yet been received by server)

Step n: Read ids in order from latest bookmark id and send to the backend in 
batches of size B
*/
function dumpNode(bookmarkNode, arr) {
  if (bookmarkNode.title) {
    // if (!bookmarkNode.children) {
    // if (String(bookmarkNode.title).indexOf(query) == -1) {
    // return $("<span></span>");
    // }
    // }
    var anchor = $("<a>");
    anchor.attr("href", bookmarkNode.url);
    anchor.text(`Title: ${bookmarkNode.title}, id: ${bookmarkNode.id}`);
    let bookmark = {
      id: bookmarkNode.id,
      title: bookmarkNode.title,
      url: bookmarkNode.url,
    };
    console.log(`bookmark: ${bookmark}`);
    arr.push(bookmark);
    // console.log(`arr: ${arr}`);
    /*
     * When clicking on a bookmark in the extension, a new tab is fired with
     * the bookmark url.
     */
    anchor.click(function () {
      chrome.tabs.create({ url: bookmarkNode.url });
    });
    var span = $("<span>");
    // Show add and edit links when hover over.
    span.append(anchor);
  }
  var li = $(bookmarkNode.title ? "<li>" : "<div>").append(span);
  if (bookmarkNode.children && bookmarkNode.children.length > 0) {
    li.append(dumpTreeNodes(bookmarkNode.children, arr));
  }
  return li;
}

// https://stackoverflow.com/questions/56478681/send-post-request-from-chrome-extension
document.addEventListener("DOMContentLoaded", function () {
  var bookmarks = [];
  dumpBookmarks(bookmarks);

  const mockStr = "someRandomTestFile.txt";
  var button = document.getElementById("submitButton");
  button.addEventListener("click", function (e) {
    e.preventDefault();
    // const data = { filename: mockStr };
    chrome.bookmarks.getTree(function () {
      // console.log(`bookmarks tree node is: ${JSON.stringify(bookmarks)}`);
      // https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
      fetch("http://localhost:5050/api/v1/bookmarks", {
        method: "POST", // or 'PUT'
        headers: {
          "Content-Type": "application/json",
        },
        mode: "cors",
        body: JSON.stringify(bookmarks),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Success:", data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });
});
