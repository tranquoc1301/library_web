// let header = `<header class="container-fluid bg-main">
//     <nav class="navbar navbar-expand-lg">
//         <div class="container">
//           <a class="navbar-brand" href="{{ url_for('index') }}">
//             <img src="{{ url_for('static', filename='images/logo.jpg') }}" width="230px" height="75px">
//           </a>
//           <div class="collapse navbar-collapse ms-3 align-items-center">
//             <ul class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 100px;">
//               <li class="nav-item">
//                 <a class="nav-link" href="{{ url_for('index') }}">Home</a>
//               </li>
//               <li class="nav-item">
//                 <a class="nav-link" href="{{ url_for('category') }}">Categories</a>
//               </li>
//               <li class="nav-item">
//                 <a class="nav-link" href="{{ url_for('book') }}">Books</a>
//               </li>
//             </ul>
//             <form class="">
//                 <div class="p-1 bg-light shadow-sm">
//                   <div class="input-group">
//                     <input type="search" placeholder="Search" class="form-control border-0 bg-light shadow-none">
//                     <div class="input-group-append">
//                       <button id="button-addon1" type="submit" class="btn btn-link text-primary"><i class="fa fa-search"></i></button>
//                     </div>
//                   </div>
//                 </div>
//               </form>
//             <div class="ms-auto">
//                 <span class="rounded-pill bg-primary px-3 py-2"><a href="{{ url_for('login') }}" class="text-light">Login</a></span>
//                 <span class="rounded-pill bg-primary px-3 py-2"><a href="{{ url_for('signup') }}" class="text-light">Register</a></span>
//             </div>
//           </div>
//         </div>
//       </nav>
// </header>`;

// document.querySelector("#header").innerHTML = header;

let footer = `<footer class="container-fluid bg-main">
    <div class="d-flex container mt-5 justify-content-between py-4 px-4">
        <div class="text-white mb-3 mb-md-0">
          Copyright © 2024. All rights reserved.
        </div>
    
        <div>
          <a href="#!" class="text-white me-4">
            <i class="fab fa-facebook-f"></i>
          </a>
          <a href="#!" class="text-white me-4">
            <i class="fab fa-twitter"></i>
          </a>
          <a href="#!" class="text-white me-4">
            <i class="fab fa-google"></i>
          </a>
          <a href="#!" class="text-white">
            <i class="fab fa-linkedin-in"></i>
          </a>
        </div>
    </div>
</footer>`;

document.querySelector("#footer").innerHTML = footer;
