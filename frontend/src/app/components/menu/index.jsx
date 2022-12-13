import React from 'react';
import { Grid } from '@mui/material';
import MenuList from '@mui/material/MenuList';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import SearchIcon from '@mui/icons-material/Search';
import ListItemText from '@mui/material/ListItemText';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import SchoolIcon from '@mui/icons-material/School';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import { Link } from 'react-router-dom';
import logo from '../../../assets/public/profile_logo.png';

const Menu = ({ auth }) => (
  <Grid container>
    <MenuList sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <img src={logo} alt="atha yoga logo" className="logo_img" />
      <MenuItem>
        <button onClick={auth.logout}>Logout</button>
      </MenuItem>
      <MenuItem>
        <ListItemIcon>
          <FavoriteBorderIcon fontSize="large" />
        </ListItemIcon>
        <ListItemText>Избранное</ListItemText>
      </MenuItem>
      <MenuItem>
        <ListItemIcon>
          <SchoolIcon fontSize="large" />
        </ListItemIcon>
        <ListItemText>Мой прогресс</ListItemText>
      </MenuItem>
      <MenuItem component={Link} to="search-lessons">
        <ListItemIcon>
          <SearchIcon fontSize="large" />
        </ListItemIcon>
        <ListItemText>Поиск</ListItemText>
      </MenuItem>
      <MenuItem component={Link} to="calendar">
        <ListItemIcon>
          <CalendarMonthOutlinedIcon fontSize="large" />
        </ListItemIcon>
        <ListItemText>Календарь</ListItemText>
      </MenuItem>
      <MenuItem component={Link} to="profile">
        <ListItemIcon>
          <AccountCircleOutlinedIcon fontSize="large" />
        </ListItemIcon>
        <ListItemText>Профиль</ListItemText>
      </MenuItem>
    </MenuList>
  </Grid>
);

export default Menu;
