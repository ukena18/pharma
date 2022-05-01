import React, {useState, useEffect} from 'react';
import { Link, useParams } from 'react-router-dom';
import useFetch from '../controllers/useFetch';
function Profile() {
    let { pk } = useParams();
    const [name,setName] = useState("Person nam");
    const [last,setLast] = useState("person last");
    const [parent_id,setParentId] = useState(0);


    const [customer,setCutomer] = useState(null)
    const [orders,setOrders] = useState(null)
    const [children,setChildren] = useState(null)

    // to get profile such as customer orders and children
    const {data,isPending,error} = useFetch(`http://127.0.0.1:8000/api/profile/${pk}`);
    // profile name change 
    const NameChange = async (e) => { 
        
        if (e.target.parent_id.value){
            setParentId(e.target.parent_id.value)
        }
        e.preventDefault();
        const response = await fetch(`http://127.0.0.1:8000/api/name_change/${pk}`,{
        method: "POST",
        headers: {
            "Content-Type":"application/json",
        },
        body: JSON.stringify({"name":name,"last":last,"parent_id":parent_id})
        
        })
        const nameData = await response.json()
        setName(()=>nameData?.customer.name)
        setLast(()=>nameData?.customer.last)

    }

    // use effect first render 
    useEffect(()=>{
        setCutomer(data?.customer)
        setOrders(data?.orders)
        setChildren(data?.children)
        setName(customer?.name)
        setLast(customer?.last)
        setParentId(parseInt(customer?.parent))
    },[data])


    
    return (
        <div>
            { isPending && <div>Loading...</div> }
            { error && <div>{ error }</div> }
            { customer ? <div>
             <div>
                    <form className="search-form edit-form" onSubmit={NameChange}>
                        <div className="order-container">
                            <Link className="search-button" style={{width:"100%"}} to={`/add_order/${customer.id}`} >Add Order</Link>
                            <h6>{customer.id}</h6>
                            
                        </div>
                        <div className="edit-container">
                            
                            <input className="input-text" type="text" id="name" name="name" value={name} onChange={(e)=>setName(e.target.value)} />
                            <input className="input-text" type="number" id="parent_id" name="parent_id" value={parent_id} onChange={(e)=>setParentId(e.target.value)} placeholder="Type Parent ID"  />
                            <input className="input-text" type="text" id="last" name="last" value={last} onChange={(e)=>setLast(e.target.value)} />
                            <input className="search-button" type="submit" value="Change" />
                        </div>
                    </form> 
            
           
                    <div className="people-list">
                        <h5 className="section-title">Most REcent Transactions</h5>
                        <div className="most-recent-nav">
                            <h6>Id</h6>
                            <h6>Name</h6>
                            <h6>Description</h6>
                            
                            <h6>Price</h6>
                            <h6>Method</h6>
                        
                        </div>
                        <hr />

                        {orders.map((order)=>{
                            return(
                                
                            <div className="single-person most-recent-nav" key={order.id}>
                                <h6><span>{order.customer.id}</span></h6>
                                <h6 className="name-tag">{order.customer.name} {order.customer.last} </h6>  
                                    <h6 >{order.description}</h6> 
                                    <h6 >{order.price} $</h6> 
                                    <button id={`pay-cash-${order.id}`} name={`pay-cash-${order.id}`} className="search-button">pCash</button>
                                    <button id={`pay-card-${order.id}`} name={`pay-card-${order.id}`} className="search-button">pCard</button>
                                    
                            </div>
                            )
                        })}
                       
                       
                       
                    </div>
            
                    <div className="people-list">
                        <h5 className="section-title">All Dependents</h5>
                        <div className="all-dependents-nav ">
                            <h6>Id</h6>
                            <h6>Name</h6>
                            <h6>Price</h6>
                            <h6>Method</h6>
                        </div>
                        <hr />
                     {children ? children.map((child)=>{
                        return(
                            <div className="single-person all-dependents-nav" key={child.id}>
                            <h6><span>{child.id}</span></h6>
                            <h6 className="name-tag">{child.name} {child.last}</h6>    
                                <h6 >{child.total} $</h6> 
                                <button id="pay-cash-1" name="pay-cash-1" className="search-button">pCash</button>
                                <button id="pay-cash-1" name="pay-cash-1" className="search-button">pCard</button> 
                        </div> 
                        )
                    }): null} 
                       
                       
                        
                    </div>
            </div> 
            
            <div className="total-amount">
                <h2>total amount:</h2>
                <h2 id="show-total-amount">{customer.total} $</h2>
            </div>
            <div className="people-list">
                    <h5 className="section-title">Transactions History</h5>
                    <div className="transactions-history-nav">
                        <h6>Id</h6>
                        <h6>Name</h6>
                        <h6>Description</h6>
                        <h6>Date paid</h6>
                        <h6>Who paid</h6>
                        <h6>Cost</h6>
                    
                    </div>
                    {orders ? orders.map((order)=>{
                        return(
                            <div className="single-person transactions-history-nav" key={order.id}>
                                <h6><span>{order.customer.id}</span></h6>
                                <h6 className="name-tag">{order.customer.name} {order.customer.last} </h6>  
                                <h6 >{order.description}</h6> 
                                {order.is_paid ? <h6>+{order.price} $</h6>:<h6>-{order.price} $</h6> }
                                {order.is_paid ? <h6>{order.customer_total_when_paid}</h6>:<h6>{order.customer_total_when_created}</h6> }
                                
                            </div>
                            )
                    }): <h1>Loading ..</h1>}
                   
            </div>
            </div> : <p>Loading</p>}
        </div>
      
    );
  }
  
  export default Profile;

