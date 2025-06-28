import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;  // we're reading this value from .env file

export const axiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true,  // this is a must - read about it below
  headers: {
    "Content-Type": "application/json",
  },
});

const login = async (email, password) => {
  const response = await axiosInstance.post('/accounts/login/', {
    email: email,
    password: password,
  });

  return response;
};

export const logoutUser = async () => {
    try {
        const response = await axiosInstance.post('/accounts/logout/', null );
        return response.data;
    }
    catch (e) {
        throw new Error("Logout failed!");
    }
    
};

export const refreshToken = async () => {
    try {
        const response = await axiosInstance.post('/accounts/refresh/', null)
        return response.data;
    }
    catch (e) {
        throw new Error("Refreshing token failed!");
    }
    
}

const resetPassword = async (email) => {
  const response = await axiosInstance.post('/accounts/resetpassword/', {
    email: email
  });

  return response;
};

const confirmResetPassword = async (email, code, new_password) => {
  const response = await axiosInstance.post('/accounts/confirmresetpassword/', {
    email: email,
    code: code,
    new_password: new_password
  });
  return response;
};

const changePassword = async (old_password, new_password) => {
  const response = await axiosInstance.post('/accounts/changepassword/', {
    old_password: old_password,
    new_password: new_password
  });
  return response;
};

const authService = { login, logoutUser, refreshToken, resetPassword, confirmResetPassword, changePassword };

export default authService;