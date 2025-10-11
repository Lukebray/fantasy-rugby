import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"
import Container from "@mui/material/Container"
import Home from "./components/Home.jsx"
import "./App.css"

function App() {
	return (
		<Router>
			<Container maxWidth="lg">
				<div>
					<ul>
						<li>
							<Link to="/home">Home</Link>
						</li>
					</ul>
				</div>

				<Routes>
					<Route path="/home" element={<Home />}></Route>
				</Routes>
			</Container>
		</Router>
	)
}

export default App
