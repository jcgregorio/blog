import std.stdio;

alias const(char)[] string;
struct test_case {
   string tpl;
   string[string] map;
   string expected;
   uint delegate(string) fn;
};

int main() {
   string[] list = ["fred", "barney"];

   string[string] empty_map;
   string[string] simple_map;
   simple_map["foo"] = "barney";

   test_case[] test_cases = [
       test_case("foo",          simple_map, "barney", (string s) { return s.length; }),
       test_case(`foo="wilma"`,  empty_map,  "barney" ),
       test_case(`foo="wilma"`,  empty_map,  "barney" )
   ];

   return 0;
}
