import { adminRoot } from './defaultValues';

const data = [
  {
    id: 'plines',
    icon: 'iconsminds-three-arrow-fork',
    label: 'menu.plines',
    to: `${adminRoot}/pline`,
    subs: [
      {
        icon: 'simple-icon-list',
        label: 'menu.plinelist',
        to: `${adminRoot}/pline/list`,
      },
    ],
  },
  {
    id: 'reports',
    icon: 'iconsminds-box-with-folders',
    label: 'menu.reports',
    to: `${adminRoot}/report`,
    // roles: [UserRole.Admin, UserRole.Editor],
    subs: [
      {
        icon: 'simple-icon-list',
        label: 'menu.reportlist',
        to: `${adminRoot}/report/list`,
      },
    ],
  },
  {
    id: 'algorithms',
    icon: 'iconsminds-formula',
    label: 'menu.algorithms',
    to: `${adminRoot}/algorithm`,
    subs: [
      {
        icon: 'simple-icon-list',
        label: 'menu.algorithmlist',
        to: `${adminRoot}/algorithm/list`,
      },
    ],
  },
  {
    id: 'development',
    icon: 'iconsminds-gears',
    label: 'menu.development',
    to: `${adminRoot}/development`,
    subs: [
      {
        icon: 'iconsminds-shuffle-2',
        label: 'menu.nodered',
        to: `http://${process.env.NODERED_IP}:${process.env.NODERED_PORT}/`,
        newWindow: true,
      },
      {
        icon: 'iconsminds-library',
        label: 'menu.sphinx',
        to: `http://${process.env.BACKEND_IP}:${process.env.BACKEND_PORT}/docs/index.html`,
        newWindow: true,
      },
      {
        icon: 'iconsminds-library',
        label: 'menu.sphinx-index',
        to: `http://${process.env.BACKEND_IP}:${process.env.BACKEND_PORT}/docs/genindex.html`,
        newWindow: true,
      },
      {
        icon: 'iconsminds-library',
        label: 'menu.redoc',
        to: `http://${process.env.BACKEND_IP}:${process.env.BACKEND_PORT}/api/schema/redoc/`,
        newWindow: true,
      },
      {
        icon: 'iconsminds-coding',
        label: 'menu.swagger',
        to: `http://${process.env.BACKEND_IP}:${process.env.BACKEND_PORT}/api/schema/swagger-ui/`,
        newWindow: true,
      },
    ],
  },
];
export default data;
