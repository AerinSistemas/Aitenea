import { all, call, fork, put, takeEvery, select } from 'redux-saga/effects';
import { getTokenConfig } from '../../helpers/Utils';
import axios from 'axios';

import { PLINE_GET_LIST, PLINE_DELETE, PLINE_GET_DETAILS,
  STEP_GET_LIST_BY_PLINE } from '../actions';

import {
  getPlineListSuccess,
  getPlineListError,
  deletePlineSuccess,
  deletePlineError,
  getPlineDetailsSuccess,
  getPlineDetailsError,
  getStepListByPlineSuccess,
  getStepListByPlineError,
} from './actions';

import { getToken } from '../auth/selectors';
import { getSelectedItems } from './selectors';

const getPlineListRequest = async (token) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      '/api/pline/', getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineListItems() {
  try {
    const token = yield select(getToken);
    const response = yield call(getPlineListRequest, token);
    yield put(getPlineListSuccess(response));
  } catch (error) {
    yield put(getPlineListError(error));
  }
}

const deletePlineRequest = async (data, token) => //{
  // eslint-disable-next-line no-return-await
  axios
    .post(
      '/api/pline/delete_bulk/', data, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* deletePline() {
  try {
    const token = yield select(getToken);
    const selectedItems = yield select(getSelectedItems);
    yield call(deletePlineRequest, selectedItems, token);
    yield put(deletePlineSuccess());
  } catch (error) {
    yield put(deletePlineError(error));
  }
}

const getPlineDetailsRequest = async (token, plineid) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/pline/${plineid}/`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineDetailsItem() {
  try {
    const token = yield select(getToken);
    const selectedItems = yield select(getSelectedItems);
    const response = yield call(getPlineDetailsRequest, token, selectedItems[0]);
    yield put(getPlineDetailsSuccess(response));
  } catch (error) {
    yield put(getPlineDetailsError(error));
  }
}

const getStepListByPlineRequest = async (token, plineid) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/steps/?pline=${plineid}`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getStepListByPlineItems() {
  try {
    const token = yield select(getToken);
    const selectedItems = yield select(getSelectedItems);
    const response = yield call(getStepListByPlineRequest, token, selectedItems[0]);
    yield put(getStepListByPlineSuccess(response));
  } catch (error) {
    yield put(getStepListByPlineError(error));
  }
}

export function* watchGetList() {
  yield takeEvery(PLINE_GET_LIST, getPlineListItems);
}

export function* watchDelete() {
  yield takeEvery(PLINE_DELETE, deletePline);
}

export function* watchGetDetails() {
  yield takeEvery(PLINE_GET_DETAILS, getPlineDetailsItem);
}

export function* watchGetStepListByPline() {
  yield takeEvery(STEP_GET_LIST_BY_PLINE, getStepListByPlineItems);
}

export default function* rootSaga() {
  yield all([fork(watchGetList)]);
  yield all([fork(watchDelete)]);
  yield all([fork(watchGetDetails)]);
  yield all([fork(watchGetStepListByPline)]);
}
