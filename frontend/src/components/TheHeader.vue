<template>
  <header class="blog-header">
    <div class="container">
      <h1>我的个人博客</h1>
      <nav>
        <a href="#">首页</a>
        <a href="#">归档</a>
        <a href="#">关于</a>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.blog-header {
  background-color: #fff;
  border-bottom: 1px solid #eee;
  padding: 20px 0;
}
.blog-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.blog-header h1 {
  margin: 0;
  font-size: 24px;
}
.blog-header nav a {
  color: #666;
  text-decoration: none;
  margin-left: 20px;
  font-weight: 500;
}
.blog-header nav a:hover {
  color: #007bff;
}
</style>