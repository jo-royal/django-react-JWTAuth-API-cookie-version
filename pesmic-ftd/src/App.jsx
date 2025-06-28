
import { useState } from "react";
import "./App.css";
import authService from "./services/api";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rEmail, setREmail] = useState("");
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [cEmail, setCEmail] = useState("");
  const [pass, setPass] = useState("");
  const [newPass, setNewPass] = useState("");

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const response = await authService.login(email, password);
    if (response.status === 200) {
      setIsLoggedIn(true);
    }
  };


  const handleLogout = async () => {
    await authService.logoutUser();
    setIsLoggedIn(false);
  };

  const handleRefresh = async () => {
    await authService.refreshToken();
    setIsLoggedIn(true);
  };


  const handleResetPassword = async (event) => {
    event.preventDefault();
    const response = await authService.resetPassword(rEmail);
    if (response.status === 200) {
      console.log("Reset email sent to:", rEmail);
    }
    else {
      console.error("Failed to send reset email");
    }
  };


  const handleConfirmResetPassword = async (e) => {
    e.preventDefault();
    console.log(cEmail, code, newPassword);
    const response = await authService.confirmResetPassword(cEmail, code, newPassword);
    if (response.status === 200) {
      console.log("Password reset successful for:", cEmail);
    } else {
      console.error("Failed to reset password");
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    try {
      await authService.changePassword(pass, newPass);
      console.log("Password reset successful for:");
    } catch (error) {
      if (error.response?.status === 401) {
        console.log("Invalid old password");
      } else {
        console.error("Failed to reset password:", error);
      }
    }
  };


  return (
    <>
      {isLoggedIn ? (
        <>
          <div>Hello {email}</div>
          <div className="h-50 bg-gray-100 items-center flex flex-col justify-center">
            <div className="bg-gray-600 p-8 flex flex-col rounded-lg">
              <h1>Welcome stranger!</h1>

              <button className="bg-blue-400 p-1 rounded-sm m-1" onClick={handleLogout}>Logout</button>

              <button className="bg-blue-400 p-1 rounded-sm m-1" onClick={handleRefresh}>refresh token</button>
            </div>
          </div>
          <form className="mt-10"
            style={{ display: "flex", flexDirection: "column" }}
            onSubmit={handleChangePassword}
          >
            <label htmlFor="pass">Old Email</label>
            <input
              className="border rounded-2xl"
              type="password"
              name="pass"
              id="pass"
              value={pass}
              onChange={(e) => setPass(e.target.value)}
              required
            />
            <label htmlFor="newPass">New Password</label>
            <input
              className="border rounded-2xl"
              type="password"
              name="newPass"
              id="newPass"
              value={newPass}
              onChange={(e) => setNewPass(e.target.value)}
              required
            />

            <button className="text-white bg-blue-400 rounded-2xl" type="submit" style={{ marginTop: "10px" }}>
              Change Password
            </button>
          </form>
        </>
      ) : (
        <>
          <div className="h-50 bg-gray-100 items-center flex flex-col justify-center">
            <div className="bg-gray-600 p-8 flex flex-col rounded-lg">
              <h1>Welcome stranger!</h1>

              <button className="bg-blue-400 p-1 rounded-sm m-1" onClick={handleRefresh}>refresh token</button>
            </div>
          </div>


          <form
            style={{ display: "flex", flexDirection: "column" }}
            onSubmit={handleFormSubmit}
          >
            <label htmlFor="email">email</label>
            <input
              className="border rounded-2xl"
              type="text"
              name="email"
              id="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
              }}
              required
            />

            <label htmlFor="password">Password</label>
            <input
              className="border rounded-2xl"
              type="password"
              name="password"
              id="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
              }}
              required
            />

            <button className="text-white bg-blue-400 rounded-2xl" type="submit" style={{ marginTop: "10px" }}>
              Login
            </button>
          </form>



          <form className="mt-10"
            style={{ display: "flex", flexDirection: "column" }}
            onSubmit={handleResetPassword}
          >
            <label htmlFor="rEmail">Reset Email</label>
            <input
              className="border rounded-2xl"
              type="email"
              name="rEmail"
              id="rEmail"
              value={rEmail}
              onChange={(e) => setREmail(e.target.value)}
              required
            />

            <button className="text-white bg-blue-400 rounded-2xl" type="submit" style={{ marginTop: "10px" }}>
              Password Reset
            </button>
          </form>



          <form
            className="mt-10"
            style={{ display: "flex", flexDirection: "column" }}
            onSubmit={handleConfirmResetPassword}
          >
            <label htmlFor="cEmail">Confirm Email</label>
            <input
              className="border rounded-2xl"
              type="email"
              name="cEmail"
              id="cEmail"
              value={cEmail}
              onChange={(e) => {
                setCEmail(e.target.value);
              }}
              required
            />

            <label htmlFor="code">Code</label>
            <input
              className="border rounded-2xl"
              type="text"
              name="code"
              id="code"
              value={code}
              onChange={(e) => {
                setCode(e.target.value);
              }}
              required
            />

            <label htmlFor="newPassword">Password</label>
            <input
              className="border rounded-2xl"
              type="password"
              name="newPassword"
              id="newPassword"
              value={newPassword}
              onChange={(e) => {
                setNewPassword(e.target.value);
              }}
              required
            />

            <button className="text-white bg-blue-400 rounded-2xl" type="submit" style={{ marginTop: "10px" }}>
              Confirm Reset Password
            </button>
          </form>
        </>
      )}

    </>
  );
};


export default App;