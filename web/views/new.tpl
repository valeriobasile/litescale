% include('header.tpl')
<h2>Create project</h2>
<form name="new" action="/new" method="post" enctype="multipart/form-data">
<label for="project_name">Project name</label>
<input name="project_name" type="text" /><br/>
<label for="phenomenon">Phenomenon (e.g., offensive, positive)</label>
<input name="phenomenon" type="text" /><br/>
<label for="tuple_size">Dimension of the tuples</label>
<select name="tuple_size">
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="4" selected="selected">4</option>
    <option value="5">5</option>
    <option value="6">6</option>
    <option value="7">7</option>
    <option value="8">8</option>
    <option value="9">9</option>
    <option value="10">10</option>
</select><br/>
<label for="replication">Replication of the instances</label>
<select name="replication">
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="4" selected="selected">4</option>
    <option value="5">5</option>
    <option value="6">6</option>
    <option value="7">7</option>
    <option value="8">8</option>
    <option value="9">9</option>
    <option value="10">10</option>
</select><br/>
<label for="instance_file">Read instances from tab-separated file</label>
<input type="file" name="instance_file" />
<input type="submit" value="create project"/>
</form>
% include('footer.tpl')
