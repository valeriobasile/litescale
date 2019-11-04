% include('header.tpl')
%if action == 'project':
<h1>Start/continue project</h1>
%else:
<h1>Generate gold standard</h1>
%end
<ul>
%for project_name in project_list:
    <li><a href="/{{action}}/{{project_name}}">{{project_name}}</a></li>
%end
</ul>
<hr/>
<a href="/">back</a>
% include('footer.tpl')
