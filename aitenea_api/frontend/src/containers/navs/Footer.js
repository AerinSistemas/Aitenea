import React from 'react';
import { Row } from 'reactstrap';
import { Colxx } from '../../components/common/CustomBootstrap';

const Footer = () => {
  return (
    <footer className="page-footer">
      <div className="footer-content">
        <div className="container-fluid">
          <Row>
            <Colxx xxs="12" sm="12">
              <p className="mb-0 text-muted">AITenea 2021</p>
            </Colxx>
          </Row>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
