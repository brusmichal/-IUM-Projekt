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
    DailyCostPredictorLinearByDuration,
    DailyCostPredictorAvg,
)
from solution.find_solution import find_solution


async def run_async_service(port: int):
    app = Application(
        [
            (r"/avg", AvgSolutionHandler),
            (r"/linear", LinearByDurationSolutionHandler),
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


class AvgSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorAvg()


class LinearByDurationSolutionHandler(SolutionHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor = DailyCostPredictorLinearByDuration()


class ABSolutionHandler(RequestHandler):
    avg_delay_predictor = AvgDelayPredictor()
    daily_cost_predictor_simple = DailyCostPredictorAvg()
    daily_cost_predictor_linear = DailyCostPredictorLinearByDuration()

    def post(self):
        try:
            a: str = self.request.headers.get("a-method")  # type: ignore
            b: str = self.request.headers.get("b-method")  # type: ignore
            if a not in {"avg", "linear"} or b not in {"avg", "linear"}:
                raise HTTPError(404)
            service_input: ServiceInput = json_decode(self.request.body)
            tracks_size = len(service_input["tracks"])
            tracks_half_at_random = set(
                random.sample(
                    [x["id"] for x in service_input["tracks"]], int(tracks_size / 2)
                )
            )
            input_a: ServiceInput = {
                "tracks": [
                    x
                    for x in service_input["tracks"]
                    if x["id"] in tracks_half_at_random
                ],
                "avg_delay_constraint": service_input["avg_delay_constraint"],
            }
            input_b: ServiceInput = {
                "tracks": [
                    x
                    for x in service_input["tracks"]
                    if x["id"] not in tracks_half_at_random
                ],
                "avg_delay_constraint": service_input["avg_delay_constraint"],
            }
            solution_a = find_solution(
                input_a,
                self.avg_delay_predictor,
                {
                    "avg": self.daily_cost_predictor_simple,
                    "linear": self.daily_cost_predictor_linear,
                }[a],
            )
            solution_b = find_solution(
                input_b,
                self.avg_delay_predictor,
                {
                    "avg": self.daily_cost_predictor_simple,
                    "linear": self.daily_cost_predictor_linear,
                }[b],
            )
            solution: ServiceOutputAB = {"a": solution_a, "b": solution_b}
            self.write(json.dumps(solution))
        except HTTPError:
            raise
        except Exception:
            traceback.print_exc()
            raise HTTPError(500)
