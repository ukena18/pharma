import React, {useContext} from 'react'
import AuthContext from '../context/AuthContext';
import Navbar from './navbar';

function Login_page() {
    const {loginUser } = useContext(AuthContext)
    return (
        <div>
            <form className="add-order-form" onSubmit={loginUser}>
                <div className="add-order-container">
                    <label for="name">Email:</label>
                    <input  className="input-text" type="text" id="email" name="email" placeholder="Type an email" />
                    
                    <label for="name">Password:</label>
                    <input  className="input-text" type="password" id="password" name="password" placeholder="Type a password" />

                    <button className="add-button search-button">Login</button>
                </div>
            </form>
        </div>
    );
  }
  
  export default Login_page;
  