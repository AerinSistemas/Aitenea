import { combineReducers } from 'redux';
import settings from './settings/reducer';
import menu from './menu/reducer';
import authUser from './auth/reducer';
import plineApp from './pline/reducer';
import reportsApp from './reports/reducer';
import algorithmApp from './algorithm/reducer';

const appReducers = combineReducers({
  menu,
  settings,
  authUser,
  plineApp,
  reportsApp,
  algorithmApp,
});

const reducers = (state, action) => {
  if (action.type === 'LOAD_USER_ERROR') {
    return appReducers(undefined, action)
  }

  return appReducers(state, action)
}

export default reducers;
