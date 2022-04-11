// eslint-disable-next-line import/no-cycle
import {
  PLINE_STATUS_GET_LIST,
  PLINE_STATUS_GET_LIST_SUCCESS,
  PLINE_STATUS_GET_LIST_ERROR,
  REPORT_GET_LIST,
  REPORT_GET_LIST_SUCCESS,
  REPORT_GET_LIST_ERROR,
  REPORT_GET_LIST_BY_PLINE,
  REPORT_GET_LIST_BY_PLINE_SUCCESS,
  REPORT_GET_LIST_BY_PLINE_ERROR,
  REPORT_GET_LIST_WITH_FILTER,
  REPORT_CHANGE_LIST_ORDER,
  REPORT_GET_LIST_WITH_ORDER,
  REPORT_GET_LIST_SEARCH,
  REPORT_SELECTED_ITEMS_CHANGE,
  REPORT_DELETE,
  REPORT_DELETE_SUCCESS,
  REPORT_DELETE_ERROR,
  REPORT_METRIC_GET_LIST,
  REPORT_METRIC_GET_LIST_SUCCESS,
  REPORT_METRIC_GET_LIST_ERROR,
  REPORT_METRIC_GET_LIST_BY_PLINE,
  REPORT_METRIC_GET_LIST_BY_PLINE_SUCCESS,
  REPORT_METRIC_GET_LIST_BY_PLINE_ERROR,
  PLINE_STATUS_GET_LIST_BY_PLINE,
  PLINE_STATUS_GET_LIST_BY_PLINE_SUCCESS,
  PLINE_STATUS_GET_LIST_BY_PLINE_ERROR,
  REPORT_GET_DETAILS,
  REPORT_GET_DETAILS_SUCCESS,
  REPORT_GET_DETAILS_ERROR,
  REPORT_METRIC_GET_LIST_BY_REPORT,
  REPORT_METRIC_GET_LIST_BY_REPORT_SUCCESS,
  REPORT_METRIC_GET_LIST_BY_REPORT_ERROR
} from '../actions';

export const getPlineStatusList = () => ({
  type: PLINE_STATUS_GET_LIST,
});

export const getPlineStatusListSuccess = (items) => ({
  type: PLINE_STATUS_GET_LIST_SUCCESS,
  payload: items,
});

export const getPlineStatusListError = (error) => ({
  type: PLINE_STATUS_GET_LIST_ERROR,
  payload: error,
});

export const getPlineReportList = () => ({
  type: REPORT_GET_LIST,
});

export const getPlineReportListSuccess = (items) => ({
  type: REPORT_GET_LIST_SUCCESS,
  payload: items,
});

export const getPlineReportListError = (error) => ({
  type: REPORT_GET_LIST_ERROR,
  payload: error,
});

export const getPlineReportListWithFilter = (column, value) => ({
  type: REPORT_GET_LIST_WITH_FILTER,
  payload: { column, value },
});

export const changePlineReportListOrder = () => ({
  type: REPORT_CHANGE_LIST_ORDER,
});

export const getPlineReportListWithOrder = (column) => ({
  type: REPORT_GET_LIST_WITH_ORDER,
  payload: column,
});

export const getPlineReportListSearch = (keyword) => ({
  type: REPORT_GET_LIST_SEARCH,
  payload: keyword,
});

export const selectedPlineReportItemsChange = (selectedItems) => ({
  type: REPORT_SELECTED_ITEMS_CHANGE,
  payload: selectedItems,
});

export const deletePlineReport = () => ({
  type: REPORT_DELETE,
});

export const deletePlineReportSuccess = () => ({
  type: REPORT_DELETE_SUCCESS,
});

export const deletePlineReportError = (error) => ({
  type: REPORT_DELETE_ERROR,
  payload: error,
});

export const getPlineReportMetricList = () => ({
  type: REPORT_METRIC_GET_LIST,
});

export const getPlineReportMetricListSuccess = (items) => ({
  type: REPORT_METRIC_GET_LIST_SUCCESS,
  payload: items,
});

export const getPlineReportMetricListError = (error) => ({
  type: REPORT_METRIC_GET_LIST_ERROR,
  payload: error,
});

export const getPlineReportListByPline = () => ({
  type: REPORT_GET_LIST_BY_PLINE,
});

export const getPlineReportListByPlineSuccess = (items) => ({
  type: REPORT_GET_LIST_BY_PLINE_SUCCESS,
  payload: items,
});

export const getPlineReportListByPlineError = (error) => ({
  type: REPORT_GET_LIST_BY_PLINE_ERROR,
  payload: error,
});

export const getPlineReportMetricListByPline = () => ({
  type: REPORT_METRIC_GET_LIST_BY_PLINE,
});

export const getPlineReportMetricListByPlineSuccess = (items) => ({
  type: REPORT_METRIC_GET_LIST_BY_PLINE_SUCCESS,
  payload: items,
});

export const getPlineReportMetricListByPlineError = (error) => ({
  type: REPORT_METRIC_GET_LIST_BY_PLINE_ERROR,
  payload: error,
});

export const getPlineStatusListByPline = () => ({
  type: PLINE_STATUS_GET_LIST_BY_PLINE,
});

export const getPlineStatusListByPlineSuccess = (items) => ({
  type: PLINE_STATUS_GET_LIST_BY_PLINE_SUCCESS,
  payload: items,
});

export const getPlineStatusListByPlineError = (error) => ({
  type: PLINE_STATUS_GET_LIST_BY_PLINE_ERROR,
  payload: error,
});

export const getPlineReportDetails = () => ({
  type: REPORT_GET_DETAILS,
});

export const getPlineReportDetailsSuccess = (item) => ({
  type: REPORT_GET_DETAILS_SUCCESS,
  payload: item,
});

export const getPlineReportDetailsError = (error) => ({
  type: REPORT_GET_DETAILS_ERROR,
  payload: error,
});

export const getPlineReportMetricListByPlineReport = () => ({
  type: REPORT_METRIC_GET_LIST_BY_REPORT,
});

export const getPlineReportMetricListByPlineReportSuccess = (items) => ({
  type: REPORT_METRIC_GET_LIST_BY_REPORT_SUCCESS,
  payload: items,
});

export const getPlineReportMetricListByPlineReportError = (error) => ({
  type: REPORT_METRIC_GET_LIST_BY_REPORT_ERROR,
  payload: error,
});