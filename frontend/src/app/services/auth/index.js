import axios from 'axios';
import storage from '../api/storage';
import { LOGIN_URL, REGISTER_URL } from './utils';
import { USER_STORAGE_KEY } from '../user/utils';

const register = ({ email, password }) => axios
  .post(REGISTER_URL, { email, password, password_confirmation: password })
  .then(response => {
    if (response.data.data.tokens.access) {
      storage.set(USER_STORAGE_KEY, response.data.data);
    }

    return response.data;
  });

const login = ({ email, password }) => axios
  .post(LOGIN_URL, { email, password })
  .then(response => {
    if (response.data.data.tokens.access) {
      storage.set(USER_STORAGE_KEY, response.data.data);
    }

    return response.data;
  });

const logout = () => {
  storage.remove(USER_STORAGE_KEY);
};

const AuthService = { register, login, logout };

export default AuthService;
