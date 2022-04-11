import { all } from 'redux-saga/effects';
import authSagas from './auth/saga';
import plineSagas from './pline/saga';
import reportsSagas from './reports/saga';
import algorithmSagas from './algorithm/saga';

export default function* rootSaga() {
  yield all([
    authSagas(),
    plineSagas(),
    reportsSagas(),
    algorithmSagas(),
  ]);
}
