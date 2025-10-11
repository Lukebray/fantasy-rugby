import { useState } from "react"
import Stack from "@mui/material/Stack"
import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Container from "@mui/material/Container"

function Home() {
	const [username, setUsername] = useState("")
	const [password, setPassword] = useState("")
	const [response, setResponse] = useState("")
	const [isLoggedIn, setIsLoggedIn] = useState(false)

	const handleLogin = () => {
		alert("Logging in...")
	}

	const handleUsernameChange = (event) => {
		setUsername(event.target.value)
	}

	const handlePasswordChange = (event) => {
		setPassword(event.target.value)
	}

	return (
		<Container maxWidth="lg">
			<Stack spacing={2} direction="column">
				<TextField
					required
					id="outlined-basic"
					label="Username"
					onChange={() => handleUsernameChange(event.target.value)}
				/>
				<TextField
					id="outlined-password-input"
					label="Password"
					type="password"
					value={password}
					onChange={() => handlePasswordChange()}
				/>
				<Button variant="contained" onClick={() => handleLogin()}>
					Login
				</Button>
				u = {username} <br></br>p ={password}
			</Stack>
		</Container>
	)
}

export default Home
