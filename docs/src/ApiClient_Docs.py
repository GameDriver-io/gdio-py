from docsgen import docsgen

from gdio.api import ApiClient

if __name__ == '__main__':
    import os

    obj = ApiClient
    methods_list = docsgen.get_methods_list(obj)

    method_template = docsgen.load_template_file(os.path.abspath('docs/src/templates/method.md'))
    class_template = docsgen.load_template_file(os.path.abspath('docs/src/templates/class.md'))

    out = docsgen.format_doc(class_template, obj, {'methods_list': methods_list})
    for method in methods_list:
        out += docsgen.format_doc(method_template, method, docsgen.get_method_doc_values(method))

    with open('docs/ApiClient_Reference.md', 'w') as f:
        f.write(out)