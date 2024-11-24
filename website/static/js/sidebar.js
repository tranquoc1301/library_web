// Toggle Sidebar
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("active");

  const content = document.querySelector(".content");
  content.classList.toggle("active");
}
