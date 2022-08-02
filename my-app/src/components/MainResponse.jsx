import React from 'react'
import { useEffect } from 'react'
import { useState } from 'react'
//import axios from 'axios'
export default function MainResponse() {
    //const myObj = {"source":"John", "dest":30, "car":null};
    const [myans,setans] = useState([])
    useEffect(()=> {
      fetch("/arbitrage").then(res =>{
        if(res.ok){
          return res.json();
        }
      
      }).then(mydata=>{
        for (let i = 0; i < Object.keys(mydata).length; i++) {
          
          console.log(mydata)
        }
        setans(mydata['oppr'])
        console.log(mydata)}).catch(err=>{console.log(err)});
    },[]);
    
    
    // useEffect(()=>{
    //   axios.get("http://localhost:5000/arbitrage")
    //   .then(res=>{
    //     console.log(res)
    //   })
    //   .catch(err=>{console.log(err)})
    // })
    //https://www.geeksforgeeks.org/how-to-build-an-html-table-using-reactjs-from-arrays/
    // const data = [
    //     { source: "USD", dest: "INR", profit: 10, time:"12 pm "},
    //     { source: "USD", dest: "AED", profit: 15, time:"3 AM" },
        
    //   ]
    // Convert JSON object send by server to java script object and use it to display out put.
    // Usestate to data retrivew from back end.pyth
    
  return (
    <div>
        <table className="table table-striped">
  <thead>
    <tr>
      
      <th scope="col">Source</th>
      <th scope="col">Destination</th>
      <th scope="col">Profit Percent</th>
      <th scope="col">Time Stamp</th>
      
    </tr>
  </thead>
  <tbody>
  {myans.map((val, key) => {
          return (
            <tr key={key}>
              <td>{val.src}</td>
              <td>{val.dst}</td>
              <td>{val.profit}</td>
              <td>{val.timestamp}</td>
            </tr>
          )
        })}

  </tbody>
</table>
    </div>
  )
}
