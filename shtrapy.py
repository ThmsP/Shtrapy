import handler
import graph
import tools
import logging

logger = tools.create_logger()

logging.info('-Create DataHandler')
dh = handler.DataHandler()
logging.info('--Process data files')
dh.process()

logging.info('-Create Graphs')
gr = graph.Graphs(dh)
logging.info('--Create pygal graphs')
gr.pygal_graphs()
logging.info('--Create term_graphs')
gr.term_graphs(2018)