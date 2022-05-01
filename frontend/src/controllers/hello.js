
import React, { useEffect } from 'react';

function Hello() {
    let getUsers = async() =>{
        let response = await fetch('http://127.0.0.1:8000/api/search', {
            method:'GET',
            headers:{
                'Content-Type':'application/json',   
            }
        })
        let data = await response.json()    
        console.log(data)
        
    }
   useEffect(()=>{
       getUsers()
   },[])
    return (
        <div>

            <h1>Hello</h1>
    </div>
    );
  }
  
  export default Hello;


