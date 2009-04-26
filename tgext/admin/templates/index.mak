<%inherit file="local:templates.master"/>

<%def name="title()">
<title>Turbogears Administration System</title>
</%def>

<%def name="content()">
    <div style="height:0px;"> &nbsp; </div>
    <h2>TurboGears Admin</h2>
    This is a fully-configurable administrative tool to help you administer your website.

    <ul>
      % for model in models:
          <li><a href='${model.lower()}s/'>${model}s</a></li>
      % endfor
    </ul>
</%def>