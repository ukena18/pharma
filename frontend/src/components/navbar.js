import React , {useContext} from 'react';
import {Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

function Navbar() {
    let {user, logoutUser} = useContext(AuthContext)
    return (
        <div>
         <header>
                <h1 className="app-title">Pharmacy APP</h1>
        </header>
        <nav className="navbar">
                <ul className="nav-list"> 
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/search">Search Person</Link></li>
                    <li><Link to="/add_person">Add person</Link></li>
                    {user ? <li><Link onClick={logoutUser} to="/login_page">Logout</Link></li>: <li><Link to="/login_page">Login</Link></li>}
                     
                </ul>
         </nav>
            
    </div>
    );
  }
  
  export default Navbar;





