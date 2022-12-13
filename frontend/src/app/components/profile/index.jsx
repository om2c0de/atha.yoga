import React, { useState } from 'react';
import { useSelector } from 'react-redux';
//  import { useNavigate, Link } from 'react-router-dom';
import MenuList from '@mui/material/MenuList';
import MenuItem from '@mui/material/MenuItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import SearchIcon from '@mui/icons-material/Search';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import SchoolIcon from '@mui/icons-material/School';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import {
  Grid,
  Box,
  Avatar,
  Badge,
  Button,
  useMediaQuery,
} from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import NotificationsNoneIcon from '@mui/icons-material/NotificationsNone';
import SettingsIcon from '@mui/icons-material/Settings';
import logo from '../../../assets/public/profile_logo.png';
import background from '../../../assets/public/profile_background.jpg';
import avatar from '../../../assets/public/profile_avatar.jpg';
import './index.scoped.scss';

const Menu = () => {
  const matches = useMediaQuery('(min-width:950px)');

  if (!matches) {
    return (
      <Grid container sx={{ width: '100vw', justifyContent: 'space-around' }}>
        <Grid item>
          <ListItemIcon>
            <SearchIcon fontSize="large" className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <FavoriteBorderIcon fontSize="large" className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <SchoolIcon fontSize="large" className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <CalendarMonthOutlinedIcon fontSize="large" className="menu_img" />
          </ListItemIcon>
        </Grid>
        <Grid item>
          <ListItemIcon>
            <AccountCircleOutlinedIcon fontSize="large" className="menu_img" />
          </ListItemIcon>
        </Grid>
      </Grid>
    );
  }
  return (
    <Grid container>
      <MenuList sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
        <img src={logo} alt="atha yoga logo" className="logo_img" />
        <MenuItem>
          <ListItemIcon>
            <SearchIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Мои занятия</ListItemText>
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
        <MenuItem>
          <ListItemIcon>
            <CalendarMonthOutlinedIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Моё расписание</ListItemText>
        </MenuItem>
        <MenuItem>
          <ListItemIcon>
            <AccountCircleOutlinedIcon fontSize="large" />
          </ListItemIcon>
          <ListItemText>Профиль</ListItemText>
        </MenuItem>
      </MenuList>
    </Grid>
  );
};

const Profile = ({ user }) => {
  const [openText, setOpenText] = useState(true);
  const matches = useMediaQuery('(min-width:950px)');

  /*
  const navigate = useNavigate();

  useEffect(() => {
    if (!Object.keys(userData).length) {
      navigate('/login');
    }
  });
*/

  return (
    <Grid
      container
      direction={matches === true ? 'row' : 'column'}
      justifyContent="flex-start"
      alignItems="flex-start"
      spacing={2}
      sx={{ paddingTop: '20px' }}
    >
      <Grid
        item
        md={2.5}
        sm={1}
        sx={{
          justifyContent: 'center', display: 'flex', borderRight: '1px solid #DCDCDC',
        }}
      >
        {matches ? <Menu /> : ''}
      </Grid>

      <Grid item md={6} sm={1} container>
        <Grid
          item
          sx={{
            marginLeft: '5%', width: '90%', display: 'flex', justifyContent: 'space-between',
          }}
        >
          <Typography component="h4" variant="h6" fontWeight="500" color="primary" sx={{ paddingBottom: '30px' }}>Профиль</Typography>
          {matches === false
            ? (
              <Box sx={{ width: '80px', display: 'flex', justifyContent: 'space-between' }}>
                <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
                  <NotificationsNoneIcon color="action" fontSize="large" />
                </Badge>
                <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
                  <SettingsIcon color="action" fontSize="large" />
                </Badge>
              </Box>
            )
            : ''}
        </Grid>
        <Card sx={{ height: '90%' }}>
          <CardMedia
            component="img"
            height="168"
            image={background}
            alt="user's background"
          />
          <CardContent>
            <Avatar
              //    alt={user.user.name}
              src={avatar}
              sx={{
                width: 128, height: 128, marginTop: '-80px', marginLeft: '30px', marginBottom: '12px',
              }}
            />
            <Typography variant="iter_h1" sx={{ paddingBottom: '3px', display: 'block' }}>Иван Иванов</Typography>
            <Typography variant="iter_h2" sx={{ paddingBottom: '20px', color: '#6C757D', display: 'block' }}>@ivan</Typography>
            <Typography variant="iter_h2" paragraph noWrap={openText}>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto corporis id
            </Typography>
            <Button variant="text" size="small" sx={{ textTransform: 'none', left: '90%', position: 'relative' }} onClick={() => setOpenText(!openText)}>
              {openText === true ? 'больше' : 'меньше'}
            </Button>
          </CardContent>
        </Card>
      </Grid>
      {matches === true
        ? (
          <Grid item md={3.5} sm={1} className="notifications_box">
            <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
              <NotificationsNoneIcon color="action" fontSize="large" />
            </Badge>
            <Badge badgeContent={4} color="primary" sx={{ cursor: 'pointer' }}>
              <SettingsIcon color="action" fontSize="large" />
            </Badge>
          </Grid>
        )
        : ''}
      {!matches ? <Grid item md={3.5} sm={1}><Menu /></Grid> : ''}
    </Grid>
  );
};

export default Profile;
