from __future__ import annotations

import asyncio
import json

from tornado.escape import json_decode
from tornado.web import Application, HTTPError, RequestHandler

from data_models import ServiceInput
from predictor.avg_delay_predictor import AvgDelayPredictor
from predictor.daily_cost_predictor import (
    DailyCostPredictor,
    DailyCostPredictorML,
    DailyCostPredictorSimple,
)
from service.solution import find_solution


async def run_service():
    app = Application(
        [(r"/simple", SimpleSolutionHandler), (r"/main", MainSolutionHandler)]
    )
    app.listen(8888)
    await asyncio.Event().wait()


def run():
    asyncio.run(run_service())


class SolutionHandler(RequestHandler):
    avg_delay_predictor: AvgDelayPredictor
    daily_cost_predictor: DailyCostPredictor

    def post(self):
        try:
            service_input = json_decode(self.request.body)
            solution = find_solution(
                service_input, self.avg_delay_predictor, self.daily_cost_predictor
            )
            self.write(json.dumps(solution))
        except HTTPError:
            raise
        except Exception as e:
            raise HTTPError(500, repr(e))


class SimpleSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorSimple()


class MainSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorML()
