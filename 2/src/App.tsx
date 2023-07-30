import {createBrowserRouter, RouterProvider} from "react-router-dom";
import {Login} from "./pages/Login";
import {Register} from "./pages/Register";
import {Home} from "./pages/Home";
import {createContext, useState} from "react";
import {UserCredential} from 'firebase/auth';
import './App.css'

const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login/>
  },
  {
    path: '/register',
    element: <Register/>
  },
  {
    path: '/',
    element: <Home/>
  }
])

interface I {
  user: UserCredential | null,
  setUser: (user: UserCredential | null) => void
}

export const Context = createContext<I>({
  user: null,
  setUser: () => {}
});

function App() {
  const [user, setUser] = useState<UserCredential | null>(null);

  return <Context.Provider value={{
    user, setUser
  }
  }>
    <RouterProvider router={router}/>
  </Context.Provider>
}

export default App
