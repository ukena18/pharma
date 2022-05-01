
import '../search.css';
import search_button from '../images/search.png';
import React, {useState,useEffect} from 'react';
import Navbar from './navbar';
import { Link } from "react-router-dom";
import useFetch from "../controllers/useFetch"


function Search() {
    const [customers,setCutomers] = useState([])
    const {data,isPending,error} = useFetch("http://127.0.0.1:8000/api/search");
    useEffect(()=>{
        setCutomers(data?.customers)
        console.log("set",customers)
    },[data])
    const submitHandler = async (e)=>{ 
        e.preventDefault()
        const response = await fetch("http://127.0.0.1:8000/api/search/",{
            method: "POST",
            headers: {
                "Content-Type":"application/json",
            },
            body:JSON.stringify({"search":e.target.search.value})
        })
        const data = await response.json()
        setCutomers(data?.customers)
    }
    return (
        <div>
            { isPending && <div>Loading...</div> }
            { error && <div>{ error }</div> }
            { customers ? <div>
               
                <div className="search-main">
                    <form className="search-form" onSubmit={submitHandler}>
                        <input className="input-text" type="text" id="search" name="search" placeholder="type a name and last" />
                        <input className="search-button" type="submit" value="Search" />
                    </form>
                    <section className="people-list">
                        <h5 className="section-title">People List</h5>
                        <div className="single-person-nav">
                            <h6>Id</h6>
                            <h6>Name</h6>
                            <h6>Cost</h6>
                        </div>
                        <hr />
                        {customers.map((customer)=>{
                            return(
                            <div className="single-person single-person-nav" key={customer.id}>
                            <h6><span>{customer.id}</span></h6>
                            <h6 className="name-tag">{customer.name} {customer.last} </h6>  
                                {/* {customer.total_owe[0] ===0 ?
                                <h6 className="person-price">NO OWE</h6> : <h6 className="person-price">{customer.total_owe[0]}</h6> }
                                 */}
                                <h6>
                                    <Link className="search-button" to={`/profile/${customer.id}`} >
                                        <img src={search_button} alt="search button" />
                                    </Link>
                                </h6>
                        </div>
                            )
                        })}
                        
                    
                    </section>
                </div>
            </div>
        : <p>Loading...</p>}
    </div>
    ); 
  }
  
  export default Search;
