import { all, call, fork, put, takeEvery, select } from 'redux-saga/effects';
import { getTokenConfig } from '../../helpers/Utils';
import axios from 'axios';

import { PLINE_STATUS_GET_LIST, REPORT_GET_LIST, REPORT_DELETE, 
  REPORT_METRIC_GET_LIST, REPORT_GET_LIST_BY_PLINE, REPORT_METRIC_GET_LIST_BY_PLINE,
  PLINE_STATUS_GET_LIST_BY_PLINE, REPORT_GET_DETAILS, REPORT_METRIC_GET_LIST_BY_REPORT 
} from '../actions';

import {
  getPlineStatusListSuccess,
  getPlineStatusListError,
  getPlineReportListSuccess,
  getPlineReportListError,
  deletePlineReportSuccess,
  deletePlineReportError,
  getPlineReportMetricListSuccess,
  getPlineReportMetricListError,
  getPlineReportDetailsSuccess,
  getPlineReportDetailsError,
} from './actions';

import { getToken } from '../auth/selectors';
import { getSelectedItems } from './selectors';
import { getCurrentPlineName, getSelectedItems as getSelectedPlineItems } from '../pline/selectors';

const getPlineStatusListRequest = async (token) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      '/api/pline_status/', getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineStatusListItems() {
  try {
    const token = yield select(getToken);
    const response = yield call(getPlineStatusListRequest, token);
    yield put(getPlineStatusListSuccess(response));
  } catch (error) {
    yield put(getPlineStatusListError(error));
  }
}

const getPlineReportListRequest = async (token) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      '/api/pline_report/', getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineReportListItems() {
  try {
    const token = yield select(getToken);
    const response = yield call(getPlineReportListRequest, token);
    yield put(getPlineReportListSuccess(response));
  } catch (error) {
    yield put(getPlineReportListError(error));
  }
}
const deletePlineReportRequest = async (data, token) => //{
  // eslint-disable-next-line no-return-await
  axios
    .post(
      '/api/pline_report/delete_bulk/', data, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* deletePlineReport() {
  try {
    const token = yield select(getToken);
    const selectedItems = yield select(getSelectedItems);
    yield call(deletePlineReportRequest, selectedItems, token);
    yield put(deletePlineReportSuccess());
  } catch (error) {
    yield put(deletePlineReportError(error));
  }
}

const getPlineReportMetricListRequest = async (token) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      '/api/pline_report_metric/', getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineReportMetricListItems() {
  try {
    const token = yield select(getToken);
    const response = yield call(getPlineReportMetricListRequest, token);
    yield put(getPlineReportMetricListSuccess(response));
  } catch (error) {
    yield put(getPlineReportMetricListError(error));
  }
}

const getPlineReportListByPlineRequest = async (token, pline_name) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/pline_report/?pline_name=${pline_name}`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineReportListByPlineItems() {
  try {
    const token = yield select(getToken);
    const currentPlineName = yield select(getCurrentPlineName);
    const response = yield call(getPlineReportListByPlineRequest, token, currentPlineName);
    yield put(getPlineReportListSuccess(response));
  } catch (error) {
    yield put(getPlineReportListError(error));
  }
}

const getPlineReportMetricListByPlineRequest = async (token, pline_name) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/pline_report_metric/?pline_name=${pline_name}`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineReportMetricListByPlineItems() {
  try {
    const token = yield select(getToken);
    const currentPlineName = yield select(getCurrentPlineName);
    const response = yield call(getPlineReportMetricListByPlineRequest, token, currentPlineName);
    yield put(getPlineReportMetricListSuccess(response));
  } catch (error) {
    yield put(getPlineReportMetricListError(error));
  }
}

const getPlineStatusListByPlineRequest = async (token, pline_id) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/pline_status/?pline=${pline_id}`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineStatusListByPlineItems() {
  try {
    const token = yield select(getToken);
    const selectedPlineItems = yield select(getSelectedPlineItems);
    const response = yield call(getPlineStatusListByPlineRequest, token, selectedPlineItems[0]);
    yield put(getPlineStatusListSuccess(response));
  } catch (error) {
    yield put(getPlineStatusListError(error));
  }
}

const getPlineReportDetailsRequest = async (token, reportid) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/pline_report/${reportid}/`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineReportDetailsItem() {
  try {
    const token = yield select(getToken);
    const selectedItems = yield select(getSelectedItems);
    const response = yield call(getPlineReportDetailsRequest, token, selectedItems[0]);
    yield put(getPlineReportDetailsSuccess(response));
  } catch (error) {
    yield put(getPlineReportDetailsError(error));
  }
}

const getPlineReportMetricListByPlineReportRequest = async (token, report) => //{
  // eslint-disable-next-line no-return-await
  axios
    .get(
      `/api/pline_report_metric/?report=${report}`, getTokenConfig(token)
    )
    .then((response) => response.data)
    .catch((error) => error);

function* getPlineReportMetricListByPlineReportItems() {
  try {
    const token = yield select(getToken);
    const selectedItems = yield select(getSelectedItems);
    const response = yield call(getPlineReportMetricListByPlineReportRequest, token, selectedItems[0]);
    yield put(getPlineReportMetricListSuccess(response));
  } catch (error) {
    yield put(getPlineReportMetricListError(error));
  }
}

export function* watchGetList() {
  yield takeEvery(REPORT_GET_LIST, getPlineReportListItems);
}

export function* watchDelete() {
  yield takeEvery(REPORT_DELETE, deletePlineReport);
}

export function* watchGetStatusList() {
  yield takeEvery(PLINE_STATUS_GET_LIST, getPlineStatusListItems);
}

export function* watchGetReportMetricList() {
  yield takeEvery(REPORT_METRIC_GET_LIST, getPlineReportMetricListItems);
}

export function* watchGetListByPline() {
  yield takeEvery(REPORT_GET_LIST_BY_PLINE, getPlineReportListByPlineItems);
}

export function* watchGetReportMetricListByPline() {
  yield takeEvery(REPORT_METRIC_GET_LIST_BY_PLINE, getPlineReportMetricListByPlineItems);
}

export function* watchGetPlineStatusListByPline() {
  yield takeEvery(PLINE_STATUS_GET_LIST_BY_PLINE, getPlineStatusListByPlineItems);
}

export function* watchGetDetails() {
  yield takeEvery(REPORT_GET_DETAILS, getPlineReportDetailsItem);
}

export function* watchGetReportMetricListByPlineReport() {
  yield takeEvery(REPORT_METRIC_GET_LIST_BY_REPORT, getPlineReportMetricListByPlineReportItems);
}

export default function* rootSaga() {
  yield all([fork(watchGetList)]);
  yield all([fork(watchDelete)]);
  yield all([fork(watchGetStatusList)]);
  yield all([fork(watchGetReportMetricList)]);
  yield all([fork(watchGetListByPline)]);
  yield all([fork(watchGetReportMetricListByPline)]);
  yield all([fork(watchGetPlineStatusListByPline)]);
  yield all([fork(watchGetDetails)]);
  yield all([fork(watchGetReportMetricListByPlineReport)]);
}
