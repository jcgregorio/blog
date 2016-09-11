var fs = require('fs');
var toMarkdown = require('to-markdown');
var path = require('path');
var mkdirp = require('mkdirp');

var walk = function(dir) {
  var results = [];
  var list = fs.readdirSync(dir)
    list.forEach(function(file) {
      file = path.join(dir, file);
      var stat = fs.statSync(file);
      if (stat && stat.isDirectory()) {
        results = results.concat(walk(file));
      } else {
        results.push(file)
      }
    })
  return results
}

var getMeta = function(src) {
  var ts = "";
  fs.readFile(src, 'utf8', function (err, data) {
    if (err) {
      console.error('Error opening file:', err.message);
      process.exit(1);
    }
    var md = toMarkdown(data, {
      converters: [
      {
        filter: 'meta',
        replacement: function(content, node) {
          ts = node.getAttribute("value");
        }
      }
      ]
    });
  });
  return ts;
}

var convert = function(src, dst) {
  fs.readFile(src, 'utf8', function (err, data) {
    if (err) {
      console.error('Error opening file:', err.message);
      process.exit(1);
    }
    data = data.replace("<!DOCTYPE html>", "");

    var title = "";
    var ts = "";
    var md = toMarkdown(data, {
      converters: [
      {
        filter: 'meta',
        replacement: function(content, node) {
          if (node.getAttribute("name") == "created") {
            ts = node.getAttribute("value");
          }
          return "";
        },
      },
      {
        filter: 'title',
        replacement: function(content, node) {
          title = content;
          return "";
        }
      }
      ]
    });
    md = ts.substring(0, 10) + " " + title + "\n\n" + md;
    if (title.length == 0) {
      console.log("Empty? :", src, ts, title);
    }

    fs.writeFile(dst, md);
  });
}

var DST = "md/";

walk('.').forEach(function(src) {
  var p = path.parse(src);
  if (p.ext == ".html") {
    var newPath = path.join(DST, p.dir);
    mkdirp(newPath, function (err) {
      if (err) {
        console.error(err);
      }
    });
    var newName = p.base.substring(0, p.base.length - p.ext.length) + ".md";
    var dst = path.join(newPath, newName);
    convert(src, dst);
  }
});
