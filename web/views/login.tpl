% include('header.tpl')
<h1>Login</h1>
<form action="/login" method="post">
    Username: <input name="user_name" type="text" />
    <input value="Login" type="submit" />
</form>
% include('footer.tpl')
