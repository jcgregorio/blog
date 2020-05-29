import std.date;
import std.string;
import std.stdio;
import std.mmfile;
import std.regexp;
import std.uri;
import array;

alias char[] str;

int main() {
    int[str][str] map;

    auto path_regex = new RegExp(r"GET /news/([a-zA-Z0-9\-\_/]+)");
    auto path_regex_prj = new RegExp(r"GET /projects/([a-zA-Z0-9\-\_]+)/ ");
    auto now = UTCtoLocalTime(getUTCtime());
    auto filename = format("/home/jcgregorio/logs/frontend/access_bitworking_org.log");
    auto file = new MmFile(filename);
    auto data = cast(str) file[];
    auto lines = std.string.split(data, "\n");
    // Chop up each line into path and referrer
    // Increment count at [path][referrer]
    foreach (s; lines) {
        // On a good log line this puts the request line at index 1 and the referrer at index 3.
        auto parts = std.string.split(s, "\"" );
        if (parts.length > 4) {
            str path;
            if (path_regex.test(parts[1])) {
                path = path_regex.match(1);
            } else if (path_regex_prj.test(parts[1])) {
                path = path_regex_prj.match(1);
            }
            if (path) {
                auto referrer = parts[3];
                map[path][referrer] += 1;
            }
        }
    }
    // At this point were done collecting the data, the
    // rest of the processing is sorting that data the
    // way we want and printing it out.

    writef("Status: 200 OK\r\n");
    writef("Content-type: text/html\r\n");
    writef("\r\n");
    writef("<html> <head> </head> <body> ");
    
    writefln("<p>%d log entries processed.</p>", lines.length);
    
    writef("<dl>");


    struct uri_count_t { 
       int count; 
       str uri; 
    }
    uri_count_t[] per_path;
    // Now sum up the hits per path
    foreach (path, referrers; map) {
        int total = 0;
        foreach (referrer, hits; referrers) {
            total += hits;
        }
        per_path ~= uri_count_t(total, path);
    }

    foreach (kvp; per_path.sort(delegate bool(uri_count_t a, uri_count_t b) { return b.count > a.count;}))  {
        writefln("<dt>%d %s</dt>", kvp.count, encode(kvp.uri));
        writefln("<dd><ul>");
        uri_count_t[] per_referrer;
        foreach (referrer; map[kvp.uri].keys.sort) {
            int hits = map[kvp.uri][referrer];
            if ("-" != referrer) {
                writefln("<li>%d <a href='%s'>%s</a></li>", hits, encode(referrer), referrer);
            }
        }
        writefln("</ul></dd>");
    }
    writefln("</dl></body>");

    return 0;
}
