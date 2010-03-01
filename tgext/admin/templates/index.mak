<%inherit file="app:templates.master"/>

<%def name="title()">
Turbogears Administration System
</%def>

<div style="height:0px;"> &nbsp; </div>
<h2>TurboGears Admin</h2>
This is a fully-configurable administrative tool to help you administer your website.

<table class="admin_grid">
  % for model in models:
    <tr py:for="model in models">
      <td>${model}s</td>
      <td>
        <a href='${model.lower()}s/new/' class="add_link">Add</a>
      </td>
      <td>
        <a href='${model.lower()}s/' class="edit_link">Edit</a>
      </td>
    </tr>
  % endfor
</table>
