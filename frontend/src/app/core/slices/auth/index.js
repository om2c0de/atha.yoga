/* eslint no-param-reassign: 0 */
import { createSlice } from '@reduxjs/toolkit';
import { user } from '../../../services/user/utils';
import registerSlice from './register';
import loginSlice from './login';
import logoutSlice from './logout';

const initialState = user
  ? { isLoggedIn: true, user }
  : { isLoggedIn: false, user: null };

const authSlice = createSlice({
  name: 'auth',
  initialState,
  extraReducers: {
    [registerSlice.fulfilled]: (state, action) => {
      state.isLoggedIn = true;
      state.user = action.payload.data.user;
      state.tokens = action.payload.data.tokens;
    },
    [registerSlice.rejected]: state => {
      state.isLoggedIn = false;
    },
    [loginSlice.fulfilled]: (state, action) => {
      state.isLoggedIn = true;
      state.user = action.payload.data.user;
      state.tokens = action.payload.data.tokens;
    },
    [loginSlice.rejected]: state => {
      state.isLoggedIn = false;
      state.user = null;
    },
    [logoutSlice.fulfilled]: state => {
      state.isLoggedIn = false;
      state.user = null;
    },
  },
});

export default authSlice.reducer;
