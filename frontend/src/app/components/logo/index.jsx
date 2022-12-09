import React from 'react';
import logo from '../../../assets/public/logo.svg';
import './style.scoped.css';

const Logo = () => (
  <div className="logo__container">
    <img src={logo} alt="logo-image" />
  </div>
);

export default Logo;
