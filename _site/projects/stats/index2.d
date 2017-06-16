import std.date;
import std.string;
import std.stdio;
import std.mmfile;
import std.regexp;
import std.uri;
import array;

alias char[] str;

int main() {
    int[str] news_map;
    int[str] projects_map;

    auto path_regex = new RegExp(r"GET /news/([a-zA-Z0-9\-\_/]+)");
    auto path_regex_prj = new RegExp(r"GET /projects/([a-zA-Z0-9\-\_]+)/ ");
    auto now = UTCtoLocalTime(getUTCtime());
    auto filename = format("/home/jcgregorio/log/bitworking.org/%04d%02d%02d.log", YearFromTime(now), MonthFromTime(now)+1, DateFromTime(now));
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
                if (path) {
                    news_map[path] += 1;
                }
            } else if (path_regex_prj.test(parts[1])) {
                path = path_regex_prj.match(1);
                if (path) {
                    projects_map[path] += 1;
                }
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
    

    struct uri_count_t { 
       int count; 
       str uri; 
    }

    uri_count_t[] per_path;
    // Now sum up the hits per path
    foreach (path, hits; news_map) {
        per_path ~= uri_count_t(hits, path);
    }

    str[] popular;
    foreach (kvp; per_path.sort(delegate bool(uri_count_t a, uri_count_t b) { return b.count > a.count;}))  {
        if (!(kvp.uri == "feed" || kvp.uri == "feed/" || kvp.uri == "comments/feed/")) {
            popular ~= kvp.uri;
        }
    }
    foreach (uri; popular[0..11]) {
        writefln("<p><a href='/news/%s'>%s</a></p>", uri, uri);
    }

    writefln("<hr/>");

    uri_count_t[] prj_per_path;
    // Now sum up the hits per path
    foreach (path, hits; projects_map) {
        prj_per_path ~= uri_count_t(hits, path);
    }

    str[] prj_popular;
    foreach (kvp; prj_per_path.sort(delegate bool(uri_count_t a, uri_count_t b) { return b.count > a.count;}))  {
        if (!(kvp.uri == "stats" || kvp.uri == "apexlearningcenter" || kvp.uri == "venus")) {
            prj_popular ~= kvp.uri;
        }
    }
    foreach (uri; prj_popular[0..11]) {
        writefln("<p><a href='/news/%s'>%s</a></p>", uri, uri);
    }



    writefln("</dl></body>");

    return 0;
}
