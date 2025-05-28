
function Header() {
  return (
    <header>
      <a href="#">
        <img src="/assets/Logo DPOnet Clara.png" alt="Logo DPOnet" id="logoHeader" />
      </a>

      <div className="user-info">
        <a className="notifications" href="#"><i className="fi fi-rs-bell"></i></a>
        <a href="#"><img src="/assets/usuario-do-circulo.png" alt="Usuário" /></a>
        <p>######## <br />##########</p>
      </div>
    </header>
  );
}

export default Header; 