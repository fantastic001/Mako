from templater.sources import *

t = DirectoryTemplateSource("template").get_template("sh/mako_system_test")
for line in open("tests.txt"):
    t.generate("tests/", {"test_name": line[:-1]})
