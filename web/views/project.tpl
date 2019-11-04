% include('header.tpl')
<script>
function annotate(id) {
    if (document.getElementById('best').value == '') {
        document.getElementById('best').value=id;
        document.getElementById('bestworst').textContent="LEAST";
        document.getElementById('instance_'+id).setAttribute("disabled", "true");
    }
    else {
        document.getElementById('worst').value=id;
        document.getElementById('instance').submit();
    }
}
</script>
<p>
    Which is the <span id="bestworst">MOST</span> {{phenomenon}}?
</p>
<div id="instances">
<form id="instance" name="instance" action="/save/{{project_name}}" method="post">
%for instance in tup:
    <input class="instance" id="instance_{{instance["id"]}}" type="button" onclick="annotate({{instance["id"]}})" value="{{instance["text"]}}"/>
%end
<input id="tup_id" name="tup_id" type="hidden" value="{{tup_id}}" />
<input id="best" name="best" type="hidden" value="" />
<input id="worst" name="worst" type="hidden" value="" />
</form>
</div>
<hr/>
{{progress}}<br/>
<a href="/">back</a>
% include('footer.tpl')
