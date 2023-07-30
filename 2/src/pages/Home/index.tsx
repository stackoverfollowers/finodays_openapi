import React, {useContext} from 'react';
import {Context} from "../../App";


export function Home(){
 const {user} = useContext(Context);

 return (
  <div>
   Вы вошли как {JSON.stringify(user?.user)}
  </div>
 )
}