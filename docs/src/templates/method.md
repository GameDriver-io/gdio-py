### <a id='{obj.__name__}'></a> {obj.__name__}({", ".join([f'{param["name"]} : `{param["type"]}`' for param in params])}) -> `{type}`

{summary}

#### Returns

{return_summary}

#### Parameters

{get_md_list_from_params_list(params, load_template_file("docs/src/templates/list.md"))}


#### Example

{example}