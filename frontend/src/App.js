import Add_order from "./components/add_order";
import Add_person from "./components/add_person";
import Homepage from "./components/homepage";
import Login_page from "./components/login_page";
import Profile from "./components/profile";
import Navbar  from "./components/navbar";
import Search from "./components/search";
import {AuthProvider} from './context/AuthContext';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import Hello from "./controllers/hello";

function App() {
  return (
    <BrowserRouter>
     <AuthProvider>
     <Navbar />
        <Routes>
        <Route path="/hello" element={<Hello /> } />
          <Route path="/" element={<Homepage/> } />
          <Route path="/add_order/:pk" element={<Add_order/> } />
          <Route path="/add_person" element={<Add_person/> } />
          <Route path="/login_page" element={<Login_page/> } />
          <Route path="/profile/:pk" element={<Profile/> } />
          <Route path="/search" element={<Search/> } />
        </Routes>
      
        </AuthProvider>
    </BrowserRouter>
  );
}

export default App;

