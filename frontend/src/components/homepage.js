
import React, {useState,useEffect} from 'react';
import search_button from '../images/search.png';
import {Link } from 'react-router-dom';


function Homepage() {
    const [common_usage, setCommonUsage] = useState([])
    const [is_paid_False, setIsPaidFalse] = useState(null)
    const [is_paid_True, setIsPaidTrue] = useState(null)
    const [most_recent_orders, setMostRecentOrders] = useState([])
    const [past_due_order, setPastDueOrder] = useState([])
    const homepage_data = async () => {
        const response = await fetch("http://127.0.0.1:8000/api/homepage_test/",{
            method: "GEt",
            headers: {
                "Content-Type":"application/json",
            },
            
        })
        const data = await response.json()
        if(response.status === 200){
            console.log(data)  
            setCommonUsage(data?.common_usage)  
            setIsPaidFalse(data?.is_paid_False)
            setIsPaidTrue(data?.is_paid_True)
            setMostRecentOrders(data?.most_recent_orders)
            setPastDueOrder(data?.past_due_order)
        }else{
            console.log("somethin went wrong status is not 200 ")
        }
    }
    useEffect(()=>{
        homepage_data()
        
    },[])
    

    return (
        <div>
        <div className="money-info">
        <h3>{is_paid_True} paid money </h3>
        <h3>{is_paid_False} unpaid money</h3>
    </div>
    <div className="index-main">
            <div className="people-list">
                <h5 className="section-title">Most REcent Transactions</h5>
                <div className="most-recent-nav">
                    <h6>Id</h6>
                    <h6>Name</h6>
                    <h6>Description</h6>
                    <h6>Price</h6>
                    <h6>Look</h6>
                </div>
                <hr />
                {most_recent_orders.map((order)=>{
                    return (
                    <div className="single-person most-recent-nav"  key={order.id}>
                        
                        <h6><span>{order.customer.id}</span></h6>
                        <h6 className="name-tag">{order.customer.name} {order.customer.last} </h6>
                        <h6 >{order.description}</h6>
                        <h6 >{order.price} $</h6>
                        <Link className="search-button" to={`/profile/${order.customer.id}`} >
                             <img src={search_button}  alt="search button" />
                        </Link>

                    </div>
                    )
                })}          
            </div>
            <div className="people-list">
                <h5 className="section-title">Past Due Transactions</h5>
                <div className="most-recent-nav">
                    <h6>Id</h6>
                    <h6>Name</h6>
                    <h6>Date Created</h6>
                    <h6>Description</h6>
                    <h6>Price</h6>
                    <h6>Look</h6>
                </div>
                <hr />
                {past_due_order ? past_due_order.map((order)=>{
                    return (
                        <div className="single-person most-recent-nav" key={order.id}>
                        <h6><span>{order.customer.id}</span></h6>
                        <h6 className="name-tag">{order.customer.name} {order.customer.last}</h6>
                        <h6>{order.date_created}</h6>
                        <h6 >{order.description}</h6>
                        <h6 >{order.price} $</h6>
                        <Link className="search-button" to={`/profile/${order.customer.id}`} >
                             <img src={search_button}  alt="search button" />
                        </Link>
    
                    </div>
                    )
                }): null}          
            </div>
            <div className="people-list">
                <h5 className="section-title">Common Usage</h5>
                <div className="most-recent-nav">
                    <h6>Id</h6>
                    <h6>Name</h6>
                    <h6>Look</h6>
                </div>
                <hr />
                {common_usage.map((customer)=>{
                    return(
                    <div className="single-person most-recent-nav">
                        <h6><span>{customer.id}</span></h6>
                        <h6 className="name-tag">{customer.name} {customer.last}</h6>
                        <Link className="search-button" to={`/profile/${customer.id}`} >
                                <img src={search_button}  alt="search button" />
                            </Link>
                    </div>
                    )}
                    )}
            
            </div>
    </div>    
    </div>
    );
  }
  
  export default Homepage;
  