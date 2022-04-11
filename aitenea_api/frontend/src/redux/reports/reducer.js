import {
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
  PLINE_STATUS_GET_LIST,
  PLINE_STATUS_GET_LIST_SUCCESS,
  PLINE_STATUS_GET_LIST_ERROR,
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

const INIT_STATE = {
  allPlineReportItems: null,
  plineReportItems: null,
  currentPlineReport: null,
  allPlineStatusItems: null,
  plineStatusItems: null,
  allPlineReportMetricItems: null,
  plineReportMetricItems: null,
  error: '',
  loading: false,
  loadingStatus: false,
  loadingMetric: false,
  filter: null,
  searchKeyword: '',
  orderDirection: 'desc',
  orderColumn: null,
  orderColumns: [
    { column: 'name', label: 'Pline name' },
    { column: 'creation_timestamp', label: 'Creation date' },
  ],
  selectedItems: [],
  reload: false,
};

export default (state = INIT_STATE, action) => {
  switch (action.type) {
    case REPORT_GET_LIST:
    case REPORT_GET_LIST_BY_PLINE:
      return { ...state, loading: false };

    case REPORT_GET_LIST_SUCCESS:
    case REPORT_GET_LIST_BY_PLINE_SUCCESS:
      return {
        ...state,
        loading: true,
        allPlineReportItems: action.payload,
        plineReportItems: action.payload,
      };

    case REPORT_GET_LIST_ERROR:
    case REPORT_GET_LIST_BY_PLINE_ERROR:
      return { ...state, loading: true, error: action.payload };

    case REPORT_GET_LIST_WITH_FILTER:
      if (action.payload.column === '' || action.payload.value === '') {
        return {
          ...state,
          loading: true,
          plineReportItems: state.allPlineReportItems,
          filter: null,
        };
      }
      // eslint-disable-next-line no-case-declarations
      const filteredItems = state.allPlineReportItems.filter(
        (item) => item[action.payload.column] === action.payload.value
      );
      return {
        ...state,
        loading: true,
        plineReportItems: filteredItems,
        filter: {
          column: action.payload.column,
          value: action.payload.value,
        },
      };

    case REPORT_CHANGE_LIST_ORDER:
      if (state.orderDirection === 'asc') {
        return { 
          ...state, 
          loading: true, 
          orderDirection: 'desc' 
        };
      }
      else {
        return { 
          ...state, 
          loading: true, 
          orderDirection: 'asc' 
        };
      }

    case REPORT_GET_LIST_WITH_ORDER:
      if (action.payload === '') {
        return {
          ...state,
          loading: true,
          plineReportItems: state.plineReportItems,
          orderColumn: null,
        };
      }

      let sortedItems = {};
      if (action.payload !== 'score') {
        // eslint-disable-next-line no-case-declarations
        sortedItems = state.plineReportItems.sort((a, b) => {
          if (a[action.payload] < b[action.payload]) return -1;
          if (a[action.payload] > b[action.payload]) return 1;
          return 0;
        });
      }
      else {
        // eslint-disable-next-line no-case-declarations
        sortedItems = state.plineReportItems.sort((a, b) => {
          // Primera métrica relacionada con cada reporte
          const metric_a = state.plineReportMetricItems.find(obj => {
            return obj.pline_report === a.id
          })
          const metric_b = state.plineReportMetricItems.find(obj => {
            return obj.pline_report === b.id
          })
          if (metric_a != undefined && metric_b != undefined) {
            if (metric_a[action.payload] < metric_b[action.payload]) return -1;
            if (metric_a[action.payload] > metric_b[action.payload]) return 1;
          }
          return 0;
        });
      }
      return {
        ...state,
        loading: true,
        plineReportItems: sortedItems,
        orderColumn: state.orderColumns.find(
          (x) => x.column === action.payload
        ),
      };

    case REPORT_GET_LIST_SEARCH:
      if (action.payload === '') {
        return { ...state, plineReportItems: state.allPlineReportItems };
      }
      // eslint-disable-next-line no-case-declarations
      const keyword = action.payload.toLowerCase();
      // eslint-disable-next-line no-case-declarations
      let searchItems = state.allPlineReportItems.filter(
        (item) =>
          item.pline_name.toLowerCase().indexOf(keyword) > -1 ||
          item.origin_dataset.toLowerCase().indexOf(keyword) > -1 ||
          item.target_dataset.toLowerCase().indexOf(keyword) > -1
      );
      return {
        ...state,
        loading: true,
        plineReportItems: searchItems,
        searchKeyword: action.payload,
      };

    case REPORT_SELECTED_ITEMS_CHANGE:
      return { ...state, loading: true, selectedItems: action.payload };

    case REPORT_DELETE:
      return { ...state, loading: false, reload: false };

    case REPORT_DELETE_SUCCESS:
      return { ...state, 
        loading: true, 
        reload: true, 
        selectedItems: []
      };

    case REPORT_DELETE_ERROR:
      return { 
        ...state, 
        loading: true, 
        reload: true, 
        selectedItems: [],
        error: action.payload 
      };

    case PLINE_STATUS_GET_LIST:
    case PLINE_STATUS_GET_LIST_BY_PLINE:
      return { ...state, loadingStatus: false };

    case PLINE_STATUS_GET_LIST_SUCCESS:
    case PLINE_STATUS_GET_LIST_BY_PLINE_SUCCESS:
      return {
        ...state,
        loadingStatus: true,
        allPlineStatusItems: action.payload,
        plineStatusItems: action.payload,
      };

    case PLINE_STATUS_GET_LIST_ERROR:
    case PLINE_STATUS_GET_LIST_BY_PLINE_ERROR:
      return { ...state, loadingStatus: true, error: action.payload };
  
    case REPORT_METRIC_GET_LIST:
    case REPORT_METRIC_GET_LIST_BY_PLINE:
    case REPORT_METRIC_GET_LIST_BY_REPORT:
      return { ...state, loadingMetric: false };

    case REPORT_METRIC_GET_LIST_SUCCESS:
    case REPORT_METRIC_GET_LIST_BY_PLINE_SUCCESS:
    case REPORT_METRIC_GET_LIST_BY_REPORT_SUCCESS:
      return {
        ...state,
        loadingMetric: true,
        allPlineReportMetricItems: action.payload,
        plineReportMetricItems: action.payload,
      };

    case REPORT_METRIC_GET_LIST_ERROR:
    case REPORT_METRIC_GET_LIST_BY_PLINE_ERROR:
    case REPORT_METRIC_GET_LIST_BY_REPORT_ERROR:
      return { ...state, loadingMetric: true, error: action.payload };

    case REPORT_GET_DETAILS:
      return { ...state, loading: false };

    case REPORT_GET_DETAILS_SUCCESS:
      return {
        ...state,
        loading: true,
        currentPlineReport: action.payload,
      };

    case REPORT_GET_DETAILS_ERROR:
      return { ...state, loading: true, error: action.payload };

    default:
      return { ...state };
  }
};
