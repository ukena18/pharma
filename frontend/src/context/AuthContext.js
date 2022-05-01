import {createContext, useState, useEffect} from "react";
import jwt_decode from "jwt-decode";
import { useNavigate } from 'react-router-dom';


const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) =>{
    const [authTokens, setAuthTokens] = useState(()=>localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null);
    const [user, setUser] = useState(()=>localStorage.getItem("authTokens") ? jwt_decode(localStorage.getItem("authTokens")) : null);
    const [loading,setLoading] = useState(false)
    let navigate = useNavigate();
    const loginUser = async (e) => {
        e.preventDefault();
        console.log("form submitted")
        console.log(e.target.email.value)
        const response = await fetch("http://127.0.0.1:8000/api/token/",{
            method: "POST",
            headers: {
                "Content-Type":"application/json",
            },
            body: JSON.stringify({"email":e.target.email.value,"password":e.target.password.value})
        })
        const data = await response.json()
        if(response.status === 200){
            setAuthTokens(data)
            console.log("myuser",jwt_decode(data.access))
            setUser(jwt_decode(data.access))
            localStorage.setItem("authTokens",JSON.stringify(data))
            navigate('/')
        }else{
            console.log("somethin went wrong status is not 200 ")
        }
    }
    const logoutUser = () => {
        setAuthTokens(null)
        setUser(null)
        localStorage.removeItem("authTokens")
        navigate("login/")
    }
    const contextData = {
        user:user,
        loginUser:loginUser,
        logoutUser,

  
    }
    

   
    return (
        <AuthContext.Provider value={contextData}>
            {loading ? null : children}
        </AuthContext.Provider>
        )
}