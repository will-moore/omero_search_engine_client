<script>
    import omeroSvg from "../lib/assets/omero.svg";
    import githubLogo from "../lib/assets/github-mark-white.svg";
    let base = import.meta.env.BASE_URL;
  </script>
  
  <!-- base element used to define relative links -->
  <base href="{base}" />
  
  <nav>
    <img alt="OMERO Logo" src={omeroSvg} />
    <h2>search engine client</h2>
    <div style="flex: 1"></div>
  
    <!-- <a href="about/"> About </a> -->
    <a class="github" title="Open in GitHub" target="_blank" href="https://github.com/ome/omero_search_engine_client/">
      <img alt="GitHub Logo" src={githubLogo} />
    </a>
  </nav>
  
  <style>
    img {
        height: 24px;
    }
    nav {
      top: 0;
      left: 0;
      width: 100%;
      display: flex;
      flex-direction: row;
      margin: 0;
      padding: 5px 15px;
      background-color: #202428;
      z-index: 20;
      align-items: center;
      box-sizing: border-box;
      flex: auto 0 0;
      gap: 5px;
    }
  
    h2 {
      color: white;
      font-weight: 300;
      margin: 2px 15px;
      font-size: 22px;
    }
    a {
      color: white;
      text-decoration: none;
      display: block;
    }
    .github img, .github {
      height: 20px;
    }
    .github {
      margin: 0 10px;
    }
  </style>
  