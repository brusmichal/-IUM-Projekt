from __future__ import annotations

import asyncio
import json
import random
import traceback

from tornado.escape import json_decode
from tornado.web import Application, HTTPError, RequestHandler

from datamodels.models import ServiceInput, ServiceOutputAB
from predictor.avg_delay_predictor import AvgDelayPredictor
from predictor.daily_cost_predictor import (
    DailyCostPredictor,
    DailyCostPredictorML,
    DailyCostPredictorSimple,
)
from solution.find_solution import find_solution


async def run_async_service(port: int):
    app = Application(
        [
            (r"/simple", SimpleSolutionHandler),
            (r"/main", MainSolutionHandler),
            (r"/ab", ABSolutionHandler),
        ]
    )
    app.listen(port)
    await asyncio.Event().wait()


def run_service(port: int):
    asyncio.run(run_async_service(port))


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
        except Exception:
            traceback.print_exc()
            raise HTTPError(500)


class SimpleSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorSimple()


class MainSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorML()


class ABSolutionHandler(RequestHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor_simple = DailyCostPredictorSimple()
    daily_cost_predictor_ml = DailyCostPredictorML()

    def post(self):
        try:
            service_input: ServiceInput = json_decode(self.request.body)
            tracks_size = len(service_input["tracks"])
            tracks_half_at_random = set(
                random.sample(
                    [x["id"] for x in service_input["tracks"]], int(tracks_size / 2)
                )
            )
            input_simple: ServiceInput = {
                "tracks": [
                    x
                    for x in service_input["tracks"]
                    if x["id"] in tracks_half_at_random
                ],
                "avg_delay_constraint": service_input["avg_delay_constraint"],
            }
            input_main: ServiceInput = {
                "tracks": [
                    x
                    for x in service_input["tracks"]
                    if x["id"] not in tracks_half_at_random
                ],
                "avg_delay_constraint": service_input["avg_delay_constraint"],
            }
            solution_simple = find_solution(
                service_input,
                self.avg_delay_predictor,
                self.daily_cost_predictor_simple,
            )
            solution_main = find_solution(
                service_input,
                self.avg_delay_predictor,
                self.daily_cost_predictor_simple,
            )
            solution: ServiceOutputAB = {
                "simple": solution_simple,
                "main": solution_main,
            }
            self.write(json.dumps(solution))
        except HTTPError:
            raise
        except Exception:
            traceback.print_exc()
            raise HTTPError(500)
